# agents/frontend_agent.py
def process_frontend_tasks(tasks):
    """
    Simulate frontend agent behavior: refine or expand UI-related tasks.
    """
    refined_tasks = []
    for task in tasks:
        if "dashboard" in task.lower():
            refined_tasks.append("Design wireframe for dashboard layout.")
            refined_tasks.append("Develop dashboard using React components.")
        elif "form" in task.lower():
            refined_tasks.append("Implement controlled form components with validation.")
            refined_tasks.append("Style forms using Tailwind CSS.")
        elif "component" in task.lower():
            refined_tasks.append("Create reusable React component structure.")
            refined_tasks.append("Integrate component into the main layout.")
        else:
            refined_tasks.append(f"Setup {task.lower()} in React environment.")

    return refined_tasks
