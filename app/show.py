import streamlit as st
import importlib

# JavaScript alert for Dark Mode suggestion
st.markdown(
    """
    <script>
        alert("💡 For better visibility and comfort, we recommend using Dark Mode in Streamlit settings (top-right menu).");
    </script>
    """,
    unsafe_allow_html=True
)

# Function to load and display content from a module
def load_and_display_module(module_name):
    try:
        module = importlib.import_module(module_name)
        return module.code()
    except ImportError:
        st.error(f"Module {module_name} not found.")
        return None

# List of page names
page_names = ["Home 🏠", "Assist 💬", "AI Model ✏️"]
selected_page = st.sidebar.selectbox("Select a page", page_names)

# Display content based on the selected tab
if selected_page == "AI Model ✏️":
    content = load_and_display_module("main")
elif selected_page == "Assist 💬":
    content = load_and_display_module("assist")
elif selected_page == "Home 🏠":
    content = load_and_display_module("source")
else:
    content = None

# Display content only if it is not None
if content is not None:
    st.write(content)

# Sidebar T&C
st.sidebar.title('Terms and Conditions 📃')
st.sidebar.markdown("""
1. **All content and intellectual property on this platform are protected by copyright; unauthorized use is strictly prohibited.**  
2. **The results provided are for informational purposes; consult a professional for medical advice.**  
3. **Privacy is prioritized; data is handled with utmost confidentiality.**
""")
