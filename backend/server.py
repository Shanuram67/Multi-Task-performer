from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash 
import os
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv() # Load variables from .env file

DB_USER = os.getenv('DATABASE_USERNAME')
DB_PASS = os.getenv('DATABASE_PASSWORD')
DB_NAME = os.getenv('DATABASE_NAME')

# Ensure we construct the URL correctly
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@localhost:5432/{DB_NAME}"

JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'a-fallback-key-for-dev') 

if not DB_USER:
    print("FATAL: Database credentials not found. Check .env file.")
    exit(1)

app = Flask(__name__)
# Allow CORS globally across all routes. Flask-CORS should handle OPTIONS requests correctly.
CORS(app, supports_credentials=True) 

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

db = SQLAlchemy(app)
jwt = JWTManager(app)

# --- Database Models (Mapping to PostgreSQL Schema) ---
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    # Define relationship to briefs
    briefs = db.relationship('ProjectBrief', backref='owner', lazy=True)

class ProjectBrief(db.Model):
    __tablename__ = 'project_briefs'
    brief_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='Pending')
    # Define relationship to tasks
    tasks = db.relationship('TechnicalTask', backref='project_brief', lazy=True)

class TechnicalTask(db.Model):
    __tablename__ = 'technical_tasks'
    task_id = db.Column(db.Integer, primary_key=True)
    brief_id = db.Column(db.Integer, db.ForeignKey('project_briefs.brief_id'), nullable=False)
    assigned_agent = db.Column(db.String(10), nullable=False) # Frontend or Backend
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='To Do')
    priority = db.Column(db.String(10), default='Medium')

# --- Helper function to serialize tasks ---
def task_serializer(task):
    return {
        'id': task.task_id,
        'title': task.description,
        'agent': task.assigned_agent,
        'status': task.status,
        'priority': task.priority,
        'brief_id': task.brief_id
    }

# --- Endpoint: Fetch Tasks (FIX: Implements missing GET /api/tasks) ---
@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_id = get_jwt_identity()
    
    # In a real scenario, this would involve complex queries joining briefs and tasks.
    # For this simulation, we fetch all tasks belonging to briefs owned by the user.
    try:
        tasks = db.session.execute(
            db.select(TechnicalTask)
            .join(ProjectBrief)
            .filter(ProjectBrief.user_id == current_user_id)
            .order_by(TechnicalTask.task_id.desc())
        ).scalars().all()
        
        # MOCK DATA INJECTION (If no tasks exist yet, simulate the Coordinator Agent's output)
        if not tasks:
             # Create initial mock tasks for a user after they log in
             mock_brief_id = 1
             tasks = [
                TechnicalTask(brief_id=mock_brief_id, assigned_agent='Backend', description='BE-001: Implement /api/auth/login', status='In Progress', priority='High'),
                TechnicalTask(brief_id=mock_brief_id, assigned_agent='Frontend', description='FE-002: Develop responsive Dashboard UI', status='To Do', priority='High'),
            ]
            
        return jsonify(tasks=[task_serializer(t) for t in tasks]), 200
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return jsonify({"msg": "Failed to retrieve tasks."}), 500

# --- Endpoint: Handle New Brief Submission ---
# backend/server.py

# ... (imports and models above) ...

# --- Endpoint: Handle New Brief Submission (Finalized) ---
@app.route('/api/briefs', methods=['POST'])
@jwt_required()
def create_brief():
    """Accepts a new high-level brief from the Frontend Agent."""
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({"msg": "Invalid or missing JWT identity."}), 401

        # Convert ID if it’s numeric-like
        try:
            current_user_id = int(current_user_id)
        except (ValueError, TypeError):
            # keep as string if not an integer
            pass

        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({"msg": "Request body must be valid JSON."}), 400

        # Extract title and description
        title = data.get('title')
        description = data.get('description')

        # Validate fields
        if not title or not description:
            return jsonify({"msg": "Both 'title' and 'description' are required."}), 400

        # Create new brief
        new_brief = ProjectBrief(
            user_id=current_user_id,
            title=str(title),
            description=str(description)
        )
        db.session.add(new_brief)
        db.session.commit()

        # Simulate coordinator tasks
        initial_tasks = [
            TechnicalTask(
                brief_id=new_brief.brief_id,
                assigned_agent='Coordinator',
                description=f"Coordinator: Review and decompose brief '{new_brief.title}'",
                status='Pending',
                priority='High'
            ),
            TechnicalTask(
                brief_id=new_brief.brief_id,
                assigned_agent='Backend',
                description="Backend: Define REST API requirements.",
                status='To Do',
                priority='Medium'
            ),
            TechnicalTask(
                brief_id=new_brief.brief_id,
                assigned_agent='Frontend',
                description="Frontend: Sketch wireframes for main views.",
                status='To Do',
                priority='Low'
            ),
        ]

        db.session.add_all(initial_tasks)
        db.session.commit()

        return jsonify({
            "msg": "Brief successfully submitted and queued for task breakdown.",
            "brief_id": new_brief.brief_id
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Brief creation failed: {e}")
        return jsonify({"msg": "Internal server error during brief creation."}), 500



# --- Endpoint: Authentication (Register & Login remain the same, ensure the models are used) ---
@app.route('/api/auth/register', methods=['POST'])
def register():
    # ... (Register logic remains the same) ...
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    if db.session.execute(db.select(User).filter_by(username=username)).first():
        return jsonify({"msg": "User already exists"}), 409
        
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        
        access_token = create_access_token(identity=str(new_user.user_id))
        # Store username in local storage for the frontend to display
        return jsonify(msg="Registration successful", access_token=access_token, username=username), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Server error during registration"}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    # ... (Login logic remains the same) ...
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    
    # FIX: Use check_password_hash with the stored hash
    if user and check_password_hash(user.password_hash, password): 
        access_token = create_access_token(identity=str(user.user_id)) 
        return jsonify(access_token=access_token, user_id=user.user_id, username=username), 200
        
    return jsonify({"msg": "Bad username or password"}), 401

@app.errorhandler(422)
def handle_unprocessable_entity(e):
    print("422 Error:", e)
    return jsonify({"msg": "Unprocessable entity", "details": str(e)}), 422


# --- Initialization ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
        
        # Mock user creation using the correct hashing logic
        if not db.session.execute(db.select(User).limit(1)).scalar():
            hashed_password = generate_password_hash('password')
            mock_user = User(username='coordinator', password_hash=hashed_password)
            db.session.add(mock_user)
            db.session.commit()
            print("Mock 'coordinator' user created (Password: 'password').")
            
    print(f"Backend Agent starting...")
    app.run(debug=True, port=5000)
