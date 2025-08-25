# streamlit_app.py (at repo root)
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
# Put the REPO ROOT first on sys.path
sys.path.insert(0, str(ROOT))

# Import the app package entry
from app import show  # this executes app/show.py
