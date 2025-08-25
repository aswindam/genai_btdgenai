# streamlit_app.py
from pathlib import Path
import sys

# Get the project root directory
ROOT = Path(__file__).resolve().parent

# Add the root directory to the Python path
sys.path.insert(0, str(ROOT))

# Import and run the show() function from the app package
# Note: We assume your show.py has a main function, let's call it 'run_app()'
from app.show import run_app

# Execute the app
if __name__ == "__main__":
    run_app()