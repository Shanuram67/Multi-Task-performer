# agents/review_agent.py
def evaluate_tasks(generated_tasks):
    """
    Review Agent:
    Evaluates and scores generated backend and frontend tasks.
    Works 100% locally — no GPT or external API.
    """

    backend_tasks = generated_tasks.get("backend", [])
    frontend_tasks = generated_tasks.get("frontend", [])
    workflows = generated_tasks.get("workflows", [])

    # --- Simple Scoring Logic ---
    scores = {
        "clarity": 0,
        "completeness": 0,
        "balance": 0
    }

    total_tasks = len(backend_tasks) + len(frontend_tasks)

    # Clarity: average sentence length (shorter = clearer)
    if total_tasks > 0:
        clarity_score = 100 - min(40, sum(len(t.split()) for t in backend_tasks + frontend_tasks) / total_tasks)
        scores["clarity"] = round(clarity_score, 2)

    # Completeness: backend or frontend missing?
    if backend_tasks and frontend_tasks:
        scores["completeness"] = 100
    elif backend_tasks or frontend_tasks:
        scores["completeness"] = 70
    else:
        scores["completeness"] = 40

    # Balance: even distribution between backend/frontend
    if backend_tasks and frontend_tasks:
        ratio = abs(len(backend_tasks) - len(frontend_tasks))
        balance_score = max(60, 100 - ratio * 10)
        scores["balance"] = balance_score
    else:
        scores["balance"] = 50

    # --- Feedback Generation ---
    feedback = []
    if scores["clarity"] < 70:
        feedback.append("Some tasks are too long or unclear. Consider rephrasing.")
    if scores["completeness"] < 100:
        feedback.append("Either backend or frontend tasks seem incomplete.")
    if scores["balance"] < 80:
        feedback.append("Uneven task distribution between backend and frontend.")
    if not feedback:
        feedback.append("Task generation looks balanced, clear, and complete!")

    return {
        "review_scores": scores,
        "feedback": feedback,
        "summary": f"Reviewed {len(backend_tasks)} backend, {len(frontend_tasks)} frontend tasks, and {len(workflows)} workflows."
    }
