# agents/frontend_agent.py
def process_frontend_tasks(text: str):
    """Detects frontend tasks from the project brief."""
    tasks = []

    if "ui" in text or "interface" in text:
        tasks.append("Design user interface components and layout.")
    if "dashboard" in text or "panel" in text:
        tasks.append("Build a responsive dashboard for managing tasks.")
    if "form" in text or "input" in text:
        tasks.append("Create input forms and connect to backend APIs.")
    if "react" in text or "frontend" in text:
        tasks.append("Set up React components and handle state management.")
    if "auth" in text or "login" in text:
        tasks.append("Build user authentication UI (login/register forms).")

    return tasks
