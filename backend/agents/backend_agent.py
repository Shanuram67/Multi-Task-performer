# agents/backend_agent.py
def process_backend_tasks(tasks):
    """
    Simulate backend agent behavior: refine backend tasks into technical actions.
    """
    refined_tasks = []
    for task in tasks:
        if "api" in task.lower():
            refined_tasks.append("Define API endpoints and routes using Flask Blueprints.")
            refined_tasks.append("Implement request validation and error handling.")
        elif "auth" in task.lower() or "login" in task.lower():
            refined_tasks.append("Setup user authentication with JWT.")
            refined_tasks.append("Secure endpoints using token-based access control.")
        elif "database" in task.lower():
            refined_tasks.append("Design normalized database schema using SQLAlchemy.")
            refined_tasks.append("Implement migration scripts with Flask-Migrate.")
        else:
            refined_tasks.append(f"Develop backend logic for {task.lower()}.")

    return refined_tasks
