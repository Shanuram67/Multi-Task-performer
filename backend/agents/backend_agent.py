# agents/backend_agent.py
def process_backend_tasks(text: str):
    """Detects backend tasks from the project brief."""
    tasks = []

    if any(k in text for k in ["auth", "login", "user", "register"]):
        tasks.append("Implement user authentication and authorization logic.")
    if "api" in text or "rest" in text:
        tasks.append("Develop REST API endpoints for CRUD operations.")
    if "database" in text or "db" in text:
        tasks.append("Design and integrate database models and schema.")
    if "server" in text or "flask" in text:
        tasks.append("Set up Flask server and handle routing.")
    if "validation" in text:
        tasks.append("Add backend validation for user inputs.")

    return tasks
