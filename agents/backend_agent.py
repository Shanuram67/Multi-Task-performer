# agents/backend_agent.py
from typing import List, Dict
from jinja2 import Environment, FileSystemLoader
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates', 'flask')

class BackendAgent:
    def __init__(self, templates_dir: str = TEMPLATES_DIR):
        self.env = Environment(loader=FileSystemLoader(templates_dir), trim_blocks=True, lstrip_blocks=True)

    def generate_backend(self, backend_tasks: List[str]) -> Dict[str, str]:
        out = {}
        for t in backend_tasks:
            key = t.lower()
            if 'authentication' in key:
                out['auth_routes.py'] = self._render('auth_routes.template.py', {})
            elif 'task management' in key or 'task' in key:
                out['task_routes.py'] = self._render('task_routes.template.py', {})
            elif 'database' in key:
                out['models.py'] = self._render('models.template.py', {})
            else:
                # a default minimal app file
                out[f"{t.replace(' ', '_')}.py"] = self._render('app_template.py', {'feature': t})
        return out

    def _render(self, template_name: str, context: dict) -> str:
        tpl = self.env.get_template(template_name)
        return tpl.render(**context)