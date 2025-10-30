# run_coordinator.py
from agents.coordinator import CoordinatorAgent
import json

if __name__ == '__main__':
    brief = "Build a task management app with user authentication and task sharing"
    c = CoordinatorAgent()
    out = c.process_brief(brief)
    print('--- FRONTEND ---')
    print('\n'.join(out['frontend'].keys()))
    print('--- BACKEND ---')
    print('\n'.join(out['backend'].keys()))

    # write artifacts to disk (optional)
    import os
    os.makedirs('generated/frontend', exist_ok=True)
    os.makedirs('generated/backend', exist_ok=True)
    for fn, code in out['frontend'].items():
        with open(os.path.join('generated/frontend', fn), 'w', encoding='utf-8') as f:
            f.write(code)
    for fn, code in out['backend'].items():
        with open(os.path.join('generated/backend', fn), 'w', encoding='utf-8') as f:
            f.write(code)
    print('Wrote generated files into ./generated/')