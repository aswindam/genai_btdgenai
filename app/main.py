import streamlit as st
from PIL import Image
import google.generativeai as genai
import base64
import warnings
from pathlib import Path
from load_dotenv import load_dotenv
import os
import streamlit.components.v1 as components


load_dotenv()

# Show modal popup on first load
# Call this once at the start of your app
components.html(
    """
    <script type="text/javascript">
        window.onload = function() {
            alert("⚠️ This app starts in Dark Mode. You can also adjust settings from the top-right menu.");
        }
    </script>
    """,
    height=0,  # no visible space taken
)



def code():
    # Creating API key from google-gemini and configuring API key
    global img
    api_key=os.getenv("genai_api_key")
    genai.configure(api_key=api_key)

    # Background image
    bg_path = Path("app/background.png")
    bg_b64 = ""
    if bg_path.exists():
        bg_b64 = base64.b64encode(bg_path.read_bytes()).decode()

    # image_path = "app/background.png"    
    # image_data = open(image_path, "rb").read()
    # image_base64 = base64.b64encode(image_data).decode()

    # Dark mode + overlay styling

    st.markdown(f"""
    <style>
    /* Background with dark overlay */
    .stApp {{
    background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)){' , url("data:image/png;base64,' + bg_b64 + '")' if bg_b64 else ''};
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}

    /* Text color */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"] * {{
    color: #f5f5f5 !important;
    }}

    /* Input box */
    .stTextInput input {{
    background-color: #1e1e1e !important;
    color: #f5f5f5 !important;
    border: 1px solid #444 !important;
    }}

    /* Text area */
    .stTextArea textarea {{
    background-color: #1e1e1e !important;
    color: #f5f5f5 !important;
    border: 1px solid #444 !important;
    }}

    /* File uploader */
    [data-testid="stFileUploader"], [data-testid="stFileUploaderDropzone"] {{
    background-color: rgba(30,30,30,0.8) !important;
    border-radius: 8px !important;
    border: 1px dashed #444 !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
    background-color: #1a1a1a !important;
    }}
    [data-testid="stSidebar"] * {{
    color: #f5f5f5 !important;
    }}

    /* Buttons */
    .stButton button {{
    background-color: #444 !important;
    color: #f5f5f5 !important;
    border: none !important;
    border-radius: 10px !important;
    }}
    .stButton button:hover {{
    background-color: #666 !important;
    color: #ffffff !important;
    }}
    </style>
    """, unsafe_allow_html=True)


    # Page title
    st.markdown(
        "<h1 style='color: skyblue; text-shadow: 4px 4px 6px rgba(0, 0, 0, 1);'>Brain Tumor Identification using AI</h1>",
        unsafe_allow_html=True)

    input_text = st.text_input('Convey what you want to ask AI here...')

    # Upload file button
    uploaded_file = st.file_uploader("**Choose a file**", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption='Uploaded Image', use_column_width=True)

    def gen_content(input_prompt, input_text, img):
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content([input_prompt, input_text, img], stream=True)
        response.resolve()
        return response

    if st.button("Check with AI"):
        if uploaded_file is not None:
            try:
                input_prompt = """
                You are an expert in analyzing and interpreting brain tumor images.
                You will receive input images for tumor classification and will be required to answer questions
                based on the information derived from those images.

                - If a question is related to other medical topics outside brain tumors, respond politely that
                  you were specifically trained in brain tumor analysis and cannot provide accurate information.
                - If a question is not medical at all, respond politely that you do not have knowledge on that subject.
                - If the user asks about your model type, internal structure, how you were trained, or who built you, respond similar with the following:
                  "I'm a custom AI model trained on 25,000+ X-ray and MRI brain scan images using Google AI Studio. My development, training, and deployment were handled by Aswin."
                """
                conclusion = gen_content(input_prompt, input_text, img)

                st.text_area("Conclusion based on your input and uploaded image",
                             value=conclusion.text, height=300, key="result_conclusion")

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please upload a file before submitting.")

    # Footer with disclaimer
    st.markdown(
        """
        ---
        #### Disclaimer:
        The predictions made by the AI model are for demonstration purposes only and should not be considered as definitive truths.  
        Always consult with a qualified professional for accurate information.  
        Model Developed: Aswin Damarapalli
        """
    )

    st.sidebar.title("Welcome to Brain Tumor Identification using AI!")
    st.sidebar.subheader(
        'This tool allows you to submit questions about brain tumor images and receive AI-generated conclusions based on your input.\n\n'
    )
    st.sidebar.title('Instructions')
    st.sidebar.write("Enter your question or input text in the text box.")
    st.sidebar.write("Upload a brain tumor image (JPG, JPEG, PNG format).")
    st.sidebar.write('Click **"Check with AI"** to get conclusions.')


if __name__ == "__main__":
    code()
