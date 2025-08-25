# app/show.py

import sys
from pathlib import Path

# --- Start of Path Correction ---
# This forces the project root onto Python's path.
# It finds the directory of this file (app/show.py), then goes up one level to the root.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# --- End of Path Correction ---


import streamlit as st
import importlib
import streamlit.components.v1 as components

# This is a diagnostic line to help debug. It will print the Python path in your app.
# st.write("Current Python Path:", sys.path)

def run_app():
    components.html(
        """
        <script type="text/javascript">
            alert("⚠️ This app starts in Dark Mode. You can also adjust settings from the top-right menu.");
        </script>
        """,
        height=0,
    )

    def load_and_display_module(module_name):
        try:
            # We will continue to use the absolute import path
            module_path = f"app.{module_name}"
            module = importlib.import_module(module_path)
            return module.code()
        except ImportError as e:
            # We'll print the module path we tried to import for clarity
            st.error(f"Failed to import module: '{module_path}'. Error: {e}")
            return None

    page_names = ["Home 🏠", "Assist 💬", "AI Model ✏️"]
    selected_page = st.sidebar.selectbox("Select a page", page_names)

    content = None
    if selected_page == "AI Model ✏️":
        content = load_and_display_module("main")
    elif selected_page == "Assist 💬":
        content = load_and_display_module("assist")
    elif selected_page == "Home 🏠":
        content = load_and_display_module("source")

    if content is not None:
        st.write(content)

    st.sidebar.title('Terms and Conditions 📃')
    st.sidebar.markdown("""
    1. **All content and intellectual property on this platform are protected by copyright; unauthorized use is strictly prohibited.**
    2. **The results provided are for informational purposes; consult a professional for medical advice.**
    3. **Privacy is prioritized; data is handled with utmost confidentiality.**
    """)

if __name__ == "__main__":
    run_app()