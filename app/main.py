import base64
from pathlib import Path

import streamlit as st
from PIL import Image

try:  # imported as part of the ``app`` package (streamlit_app.py entry point)
    from app import llm
except ImportError:  # run directly from inside the app/ directory
    import llm


DEFAULT_QUESTION = ("Analyse this scan and describe any tumour related findings, "
                    "including location and type if visible.")


def code():
    # Custom CSS for background image
    # Read the image file
    image_path = Path(__file__).with_name("background.png")
    image_data = image_path.read_bytes()

    # Convert the image data to base64
    image_base64 = base64.b64encode(image_data).decode()

    # Set the background image using a container with custom style
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: linear-gradient(rgba(6, 12, 28, 0.82), rgba(6, 12, 28, 0.90)),
                                  url('data:image/png;base64,{image_base64}');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Page title
    st.markdown(
        "<h1 style='color: skyblue; text-shadow: 4px 4px 6px rgba(0, 0, 0, 1);'>Brain Tumor Identification using AI</h1>",
        unsafe_allow_html=True)

    input_text = st.text_input('Convey what you want to ask AI here...')

    # Upload file button
    uploaded_file = st.file_uploader("**Choose a file**", type=["jpg", "jpeg", "png"])

    check = st.button('Generate Image')

    # Derive the image from the upload itself, so that "Check with AI" works
    # even when "Generate Image" was never pressed.
    img = Image.open(uploaded_file) if uploaded_file is not None else None

    if img is not None and check:
        st.image(img, caption='Uploaded Image', use_column_width=True)

    def gen_content(input_prompt, input_text, img):
        # An empty text block is rejected by the API, so fall back to a default.
        question = (input_text or '').strip() or DEFAULT_QUESTION
        return llm.generate(prompt=question, system=input_prompt, image=img)

    if st.button("Check with AI"):
        if uploaded_file is not None:
            try:
                input_prompt = """
                               You are an expert in understanding tumors in the brain.
                               You will receive input images to classify tumors, 
                               and you will have to answer questions based on the input image.
                               """
                with st.spinner("Analysing the scan..."):
                    conclusion = gen_content(input_prompt, input_text, img)

                st.subheader("Conclusion based on your input and uploaded image")
                # A bordered container keeps the markdown formatting intact
                # (headings, bullets, bold) instead of printing it literally,
                # and the dark theme gives it a readable card look by default.
                with st.container(border=True):
                    st.markdown(conclusion)

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
