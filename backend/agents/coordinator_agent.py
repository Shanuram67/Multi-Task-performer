# agents/coordinator_agent.py
from .frontend_agent import process_frontend_tasks
from .backend_agent import process_backend_tasks

# --- Keyword patterns for task detection ---
BACKEND_KEYWORDS = ["api", "database", "auth", "server", "backend", "rest", "graphql", "validation"]
FRONTEND_KEYWORDS = ["ui", "page", "dashboard", "form", "button", "frontend", "component", "responsive"]


def generate_tasks_from_brief(title: str, description: str):
    """
    Analyze the brief text and generate relevant technical tasks
    for Backend and Frontend agents (local AI simulation).
    """
    text = f"{title} {description}".lower()
    backend_tasks = []
    frontend_tasks = []

    # --- Backend task detection ---
    if any(k in text for k in BACKEND_KEYWORDS):
        backend_tasks.append("Design and implement REST API endpoints.")
    if "auth" in text or "login" in text:
        backend_tasks.append("Setup user authentication and JWT-based session handling.")
    if "database" in text or "data" in text:
        backend_tasks.append("Design and migrate database schema.")
    if "api" in text:
        backend_tasks.append("Integrate external or internal API services.")

    # --- Frontend task detection ---
    if any(k in text for k in FRONTEND_KEYWORDS):
        frontend_tasks.append("Build a responsive dashboard UI.")
    if "form" in text or "input" in text:
        frontend_tasks.append("Create interactive forms with validation.")
    if "task" in text or "project" in text:
        frontend_tasks.append("Implement task creation and listing page.")
    if "component" in text:
        frontend_tasks.append("Develop reusable UI components using React.")

    # --- Default fallbacks ---
    if not backend_tasks:
        backend_tasks.append("Setup basic backend structure with Flask.")
    if not frontend_tasks:
        frontend_tasks.append("Setup basic frontend UI layout.")

    # --- Refine tasks using agents ---
    backend_tasks = process_backend_tasks(backend_tasks)
    frontend_tasks = process_frontend_tasks(frontend_tasks)

    # --- Return structured output ---
    return {
        "backend": backend_tasks,
        "frontend": frontend_tasks
    }
