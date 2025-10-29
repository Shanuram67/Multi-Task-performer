from agents.coordinator import CoordinatorAgent

def test_basic_brief():
    c = CoordinatorAgent()
    out = c.process_brief('Build a task app with auth and tasks')
    assert 'Login.jsx' in out['frontend']
    assert 'Dashboard.jsx' in out['frontend']
    assert 'auth_routes.py' in out['backend'] or 'Auth' in '\n'.join(out['backend'].keys())