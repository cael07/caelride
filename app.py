import sys
import os
import time

# Set global application timezone to Asia/Manila (Philippine Standard Time, UTC+8)
os.environ['TZ'] = 'Asia/Manila'
if hasattr(time, 'tzset'):
    try:
        time.tzset()
    except Exception:
        pass

# Add the 'backend' directory to the Python path
# This allows 'import database' and other top-level imports in the backend to work correctly
backend_path = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, backend_path)

# Import the FastAPI app from backend/main.py as a package
try:
    from backend.main import app
except ImportError as e:
    print(f"Error: Could not find 'main.py' in {backend_path}")
    raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

