import streamlit as st
from PIL import Image
import google.generativeai as genai
import base64
from st_pages import Page, add_page_title, show_pages, hide_pages

def code():

    # Creating API key from google-gemini and configuring API key
    api_key = 'AIzaSyB9eNsm-iOLawbIm-yvuD7vmMsD5IDF1bY'
    genai.configure(api_key=api_key)

    # Custom CSS for background image
    # Read the image file
    image_path = "background.png"
    image_data = open(image_path, "rb").read()

    # Convert the image data to base64
    image_base64 = base64.b64encode(image_data).decode()

    # Set the background image using a container with custom style
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url('data:image/png;base64,{image_base64}');
                background-size: cover;
                background-repeat: no-repeat;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Page title
    st.markdown("<h1 style='color: skyblue; text-shadow: 4px 4px 4px rgba(0, 0, 0, 0.8);'>Brain Tumor Identification using AI</h1>", unsafe_allow_html=True)

    input_text = st.text_input('Convey what you want to ask AI here...')

    # Upload file button
    uploaded_file = st.file_uploader("**Choose a file**", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption='Uploaded Image', use_column_width=True)

    def gen_content(input_prompt, input_text, img):
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([input_prompt, input_text, img], stream=True)
        response.resolve()
        conclusion = response.text
        return conclusion

    if st.button("Check with AI"):
        if uploaded_file is not None:
            try:
                input_prompt = """
                               You are an expert in understanding tumors in the brain.
                               You will receive input images to classify tumors, 
                               and you will have to answer questions based on the input image.
                               """
                conclusion = gen_content(input_prompt, input_text, img)

                # Display the result
                result = st.text_area("Conclusion based on your input and uploaded image", value=conclusion, height=300,
                             key="result_conclusion")
                st.write(result)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please upload a file before submitting.")

    # Footer with disclaimer
    st.markdown(
        """
        ---
        #### Disclaimer:
        The predictions made by the AI model are for demonstration purposes only and should not be considered as definitive truths. Always consult with a qualified professional for accurate information.  
        Model Developed: Aswin Damarapalli
        """
    )

    st.sidebar.title("Welcome to Brain Tumor Identification using AI! This tool allows you to submit questions about "
                     "brain tumor images and receive AI-generated conclusions based on your input.\n\n")

    hide_pages([Page('main.py')])

    show_pages(
        [
            Page("source.py", "About", "🏠"),
            Page("assist.py", "Assistant", "🤖")
        ]
    )

    st.sidebar.title('Instructions')
    st.sidebar.write(
        "Enter your question or input text in the text box, Pass the instructions Carefully to AI.")
    st.sidebar.write(
        'Upload a brain tumor image (in JPG, JPEG, or PNG format), You can upload X-ray, MRI or any other Scan Report')
    st.sidebar.write(
        'Click the "Check with AI" button to get AI-generated conclusions.')


if __name__ == "__main__":
    code()
