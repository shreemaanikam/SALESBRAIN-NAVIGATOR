import sys
import os

# The Vercel python builder runs from the "root" specified in vercel.json.
# If "root": "backend", then the current working directory is the 'backend' folder.
# The code imports 'backend.app.main', meaning it expects a 'backend' module in sys.path.
# We can dynamically create a 'backend' module that points to the current directory.
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.dirname(current_dir)

# Add parent directory to sys.path so 'backend' can be found.
# Vercel might not include the parent directory in the deployment if root="backend".
# But if it does, this works. If it doesn't, we can alias it:
if not os.path.exists(os.path.join(parent_dir, 'backend')):
    import importlib.util
    import importlib.machinery
    spec = importlib.machinery.ModuleSpec('backend', None, is_package=True)
    backend_module = importlib.util.module_from_spec(spec)
    backend_module.__path__ = [current_dir]
    sys.modules['backend'] = backend_module

sys.path.insert(0, parent_dir)

from backend.app.main import app
