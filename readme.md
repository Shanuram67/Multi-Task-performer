# 🤖 AI Agent Task Management System

An advanced **AI-driven Agent Platform** that converts high-level project briefs into **technical tasks**, managed by specialized AI agents — including **Coordinator**, **Frontend**, **Backend**, and **Review** agents.  
Built with a professional **React + Vite** frontend and a **Python backend**, this system offers a complete task automation workflow, authentication, and responsive UI design.

---

## 🌟 Core Features

- 🧠 **AI Coordinator Agent**
  - Accepts high-level project briefs.
  - Breaks them into actionable technical tasks.
  - Delegates tasks to specialized agents (Frontend, Backend, Review).
- 💻 **Frontend Agent**
  - Generates React component structures and UI layouts.
  - Ensures responsive, accessible, and consistent design.
- ⚙️ **Backend Agent**
  - Builds REST/GraphQL APIs.
  - Handles authentication, validation, and database schema generation.
- 🧾 **Review Agent**
  - Reviews generated code and responses for correctness and optimization.
  - Ensures quality before sending results back to Coordinator.
- 🧑‍💼 **Admin Dashboard**
  - Displays all project briefs and generated tasks.
  - Tabular and card-based responsive layout.
- 🔐 **Agent Authentication**
  - Secure login & profile creation system.
- 🪶 **Beautiful UI/UX**
  - Centered login and dashboard views with modals and modern typography.
  - Custom color palette and CSS responsiveness.

---

## 🧩 AI Agent Architecture

### **Coordinator Agent**
| Function | Description |
|-----------|-------------|
| Input | High-level project brief |
| Processing | Uses regex + AI logic to classify task type |
| Delegation | Sends frontend tasks to `frontend_agent.py` and backend tasks to `backend_agent.py` |
| Output | Consolidated code snippets for frontend & backend |

---

### **Frontend Agent**
| Capability | Description |
|-------------|-------------|
| Framework | React (Vite + JSX) |
| Responsibility | Converts UI-related requirements into components |
| Output | Component files, layout suggestions, responsive hooks |
| Keywords Trigger | `ui`, `component`, `dashboard`, `modal`, `form`, `layout` |

---

### **Backend Agent**
| Capability | Description |
|-------------|-------------|
| Framework | Flask / FastAPI |
| Responsibility | Builds REST APIs, handles database logic |
| Output | Routes, models, and API structure |
| Keywords Trigger | `api`, `database`, `auth`, `server`, `validation`, `REST` |

---

### **Review Agent (Future Integration)**
| Function | Description |
|-----------|-------------|
| Input | Tasks completed by other agents |
| Processing | Evaluates correctness, readability, optimization |
| Output | Suggests improvements and final review summary |

---

## 🧰 Tech Stack

| Layer | Technology |
|--------|-------------|
| Frontend | React + Vite + Lucide React |
| Backend | Python (Flask / FastAPI) |
| Database | MongoDB / PostgreSQL |
| Styling | Custom CSS (`styles.css`) |
| AI Agents | Python-based modular scripts |
| Authentication | JWT / Clerk (optional) |

---



## 🎨 Styling Highlights

All visual design handled in:
```

frontend/src/app.css

````

Includes:
- Responsive grid & card layout  
- Centralized authentication card  
- Clean table layout for dashboard  
- Modal transitions and shadows for premium UI feel  

---

## 🚀 Getting Started

### 🧱 1. Clone Repository
```bash
git clone https://github.com/Shanuram67/Multi-Task-performer

````

### ⚙️ 2. Install Dependencies

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

**Backend**

```bash
cd backend
pip install -r requirements.txt
python main.py
```

---

## 🌐 API Endpoints (Backend)

| Method | Endpoint               | Description              |
| ------ | ---------------------- | ------------------------ |
| `POST` | `/api/briefs`          | Submit new project brief |
| `GET`  | `/api/briefs`          | Fetch all briefs         |
| `POST` | `/api/agents/login`    | Agent authentication     |
| `POST` | `/api/agents/register` | Create new agent profile |
| `GET`  | `/api/review`          | Review completed tasks   |

---

## 📋 Environment Variables

Create `.env` in `/backend`:

```
PORT=5000
MONGO_URI=mongodb://localhost:27017/ai_agent_db
JWT_SECRET=your_secret_key
```

---

## 🧠 AI Logic Summary

* Coordinator Agent uses keyword-based classification to identify task type.
* Each sub-agent (`frontend`, `backend`, `review`) processes tasks independently.
* Coordinator merges final results into one response.
* Output is displayed in the Dashboard UI in tabular or card view.

---

## 🧾 License

Licensed under the **MIT License** — free to use and modify.

---

## 👨‍💻 Author

**Developed by:** Shanmukha Satya
🧩 **Full Stack Developer | AI & ML Enthusiast**
🌐 [Portfolio](https://seeram-portfolio.netlify.app/)
💼 Skilled in **MERN Stack**, **Python**, and **Machine Learning**

---

```

---

