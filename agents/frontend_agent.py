from typing import List, Dict
from jinja2 import Environment, FileSystemLoader
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates', 'react')

class FrontendAgent:
    def __init__(self, templates_dir: str = TEMPLATES_DIR):
        self.env = Environment(loader=FileSystemLoader(templates_dir), trim_blocks=True, lstrip_blocks=True)

    def generate_ui_components(self, ui_tasks: List[str]) -> Dict[str, str]:
        out = {}
        for t in ui_tasks:
            key = t.lower()
            if 'login' in key:
                out['Login.jsx'] = self._render('Login.jsx.template', {})
            elif 'dashboard' in key or 'task dashboard' in key:
                out['Dashboard.jsx'] = self._render('Dashboard.jsx.template', {})
            else:
                filename = f"{t.replace(' ', '')}.jsx"
                out[filename] = self._render('GenericComponent.jsx.template', {'component_name': t.replace(' ', '')})
        return out

    def _render(self, template_name: str, context: dict) -> str:
        tpl = self.env.get_template(template_name)
        return tpl.render(**context)