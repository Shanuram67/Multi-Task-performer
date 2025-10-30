from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from models import db, User, ProjectBrief, TechnicalTask
from agents.coordinator_agent import generate_tasks_from_brief
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

DB_USER = os.getenv('DATABASE_USERNAME')
DB_PASS = os.getenv('DATABASE_PASSWORD')
DB_NAME = os.getenv('DATABASE_NAME')
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@localhost:5432/{DB_NAME}"

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', 'supersecretkey')  # 👈 add a secret
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# --- MODELS ---
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    briefs = db.relationship('ProjectBrief', backref='owner', lazy=True)

class ProjectBrief(db.Model):
    __tablename__ = 'project_briefs'
    brief_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='Pending')
    tasks = db.relationship('TechnicalTask', backref='project_brief', lazy=True)

class TechnicalTask(db.Model):
    __tablename__ = 'technical_tasks'
    task_id = db.Column(db.Integer, primary_key=True)
    brief_id = db.Column(db.Integer, db.ForeignKey('project_briefs.brief_id'), nullable=False)
    assigned_agent = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='To Do')
    priority = db.Column(db.String(10), default='Medium')


# --- AUTH ---
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username, password = data.get('username'), data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 409

    hashed = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Registration successful"}), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username, password = data.get('username'), data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        token = create_access_token(identity=username)
        return jsonify({
            "msg": "Login successful",
            "access_token": token,
            "username": username
        }), 200
    return jsonify({"msg": "Invalid credentials"}), 401



# --- CREATE NEW BRIEF (No JWT) ---
@app.route('/api/briefs', methods=['POST'])
def create_brief():
    data = request.get_json()
    username = data.get('username')
    title = data.get('title')
    description = data.get('description')

    if not username or not title or not description:
        return jsonify({"msg": "Missing fields"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Save new brief
    new_brief = ProjectBrief(user_id=user.user_id, title=title, description=description)
    db.session.add(new_brief)
    db.session.commit()

    # Generate tasks using our local AI agent
    generated = generate_tasks_from_brief(title, description)

    # Store dynamic tasks
    for desc in generated["backend"]:
        db.session.add(TechnicalTask(brief_id=new_brief.brief_id, assigned_agent="Backend", description=desc, priority="High"))
    for desc in generated["frontend"]:
        db.session.add(TechnicalTask(brief_id=new_brief.brief_id, assigned_agent="Frontend", description=desc, priority="Medium"))

    db.session.commit()

    return jsonify({
        "msg": "Brief created successfully",
        "brief_id": new_brief.brief_id,
        "tasks": generated
    }), 201

# --- GET TASKS (by username) ---
@app.route('/api/tasks/<username>', methods=['GET'])
def get_tasks(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    tasks = (
        db.session.query(TechnicalTask)
        .join(ProjectBrief, ProjectBrief.brief_id == TechnicalTask.brief_id)
        .filter(ProjectBrief.user_id == user.user_id)
        .order_by(TechnicalTask.task_id.desc())
        .all()
    )

    serialized = [{
        "id": t.task_id,
        "title": t.description,
        "agent": t.assigned_agent,
        "status": t.status,
        "priority": t.priority
    } for t in tasks]

    return jsonify({"tasks": serialized}), 200


# --- INIT ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
