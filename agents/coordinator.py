# agents/coordinator.py
from typing import Tuple, List, Dict
from .frontend_agent import FrontendAgent
from .backend_agent import BackendAgent
import re

class CoordinatorAgent:
    """Coordinator that parses brief -> subtask list -> dispatches to agents."""
    def __init__(self):
        self.frontend = FrontendAgent()
        self.backend = BackendAgent()

    def process_brief(self, brief: str) -> Dict[str, Dict[str, str]]:
        """Main entry. Returns a dict: { 'frontend': {filename: code}, 'backend': {filename: code} }"""
        frontend_tasks, backend_tasks = self._analyze_brief(brief)

        frontend_output = self.frontend.generate_ui_components(frontend_tasks)
        backend_output = self.backend.generate_backend(backend_tasks)

        # Optionally run a lightweight review pass
        self._review_outputs(frontend_output, backend_output)

        return {
            'frontend': frontend_output,
            'backend': backend_output
        }

    def _analyze_brief(self, brief: str) -> Tuple[List[str], List[str]]:
        b = brief.lower()
        f_tasks, bk_tasks = [], []

        # keywords mapping - extendable
        if re.search(r"auth|authentication|login|signup|register", b):
            bk_tasks.append('User Authentication API')
            f_tasks.append('Login Page')

        if re.search(r"task|todo|task management|tasks", b):
            bk_tasks.append('Task Management API')
            f_tasks.append('Task Dashboard')

        if re.search(r"share|sharing|collaborat", b):
            bk_tasks.append('Task Sharing API')
            f_tasks.append('Share Dialog')

        if re.search(r"profile|user profile", b):
            bk_tasks.append('User Profile API')
            f_tasks.append('Profile Page')

        # default/general
        if not f_tasks and not bk_tasks:
            # minimal scaffold
            bk_tasks.append('Basic REST API')
            f_tasks.append('Landing Page')

        # database implied
        if re.search(r"database|persist|store|sqlite|postgres|mongo", b) or 'api' in b:
            bk_tasks.append('Database Schema')

        return f_tasks, bk_tasks

    def _review_outputs(self, fe: Dict[str, str], be: Dict[str, str]):
        # lightweight checks — ensure no empty artifacts
        for name, code in {**fe, **be}.items():
            if not code.strip():
                raise ValueError(f"Empty artifact produced for {name}")