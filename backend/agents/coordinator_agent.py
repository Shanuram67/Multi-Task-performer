# agents/coordinator_agent.py
from .frontend_agent import process_frontend_tasks
from .backend_agent import process_backend_tasks
from .review_agent import evaluate_tasks
import re

def clean_text(text):
    """Normalize brief text for easier keyword matching."""
    return re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())

def generate_tasks_from_brief(title: str, description: str):
    """
    Local AI Coordinator — No GPT key required.
    Splits the given project brief into structured backend and frontend tasks.
    """

    text = clean_text(f"{title} {description}")

    backend_ideas = process_backend_tasks(text)
    frontend_ideas = process_frontend_tasks(text)

    # Basic business logic: auto-include extra steps based on keywords
    business_workflows = []

    if "auth" in text or "login" in text:
        business_workflows.append("Design user authentication workflow (register/login/logout).")

    if "task" in text or "project" in text:
        business_workflows.append("Create task scheduling and status management workflow.")

    if "data" in text or "database" in text:
        business_workflows.append("Set up data validation and persistence layer in the database.")

    if not backend_ideas and not frontend_ideas:
        # fallback if text too generic
        backend_ideas = [
            "Set up basic REST API structure.",
            "Implement user model and database connection.",
        ]
        frontend_ideas = [
            "Design main UI layout with navigation bar and sections.",
            "Create forms for input and submission.",
        ]

    return {
        "backend": backend_ideas + business_workflows,
        "frontend": frontend_ideas,
        "workflows": business_workflows
    }
    
    output = {
        "backend": backend_ideas + business_workflows,
        "frontend": frontend_ideas,
        "workflows": business_workflows
    }

    # NEW: Pass through review agent
    review = evaluate_tasks(output)
    output["review"] = review

    return output
# Example usage:
# tasks = generate_tasks_from_brief("Build a Task Manager", "Create a web app with user login and task scheduling.")
# print(tasks)