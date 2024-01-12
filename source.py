from pathlib import Path
import streamlit as st
from st_pages import Page, add_page_title, show_pages, hide_pages
import base64

image_path = "first.png"
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
            opacity: 0.6;
        }}
        body {{
            color: #333; /* Change text color to a darker shade */
        }}
    </style>
    """,
    unsafe_allow_html=True
)

hide_pages([Page('source.py')])

show_pages(
    [
        Page("main.py", "AI Model", '💬'),
        Page("assist.py", "Assistant", "✏️")
    ]
)

add_page_title('Brain Tumor Identification using AI')

# Gen AI Section
st.title("Gen AI: Unleashing the Power of Artificial Intelligence")

st.markdown(
    """
    <div style="color: white; filter: brightness(150%);">
        In the ever-evolving landscape of artificial intelligence, one standout player making waves is Gen AI.<br>
        Gen AI represents the cutting-edge integration of advanced machine learning algorithms and powerful data processing capabilities.<br>
        Developed by leading minds in the field, Gen AI is at the forefront of pushing the boundaries of what's possible in AI applications.
    </div>
    """,
    unsafe_allow_html=True
)

# Brain Tumor Identification Model Section
st.title("Brain Tumor Identification Model: Revolutionizing Medical Diagnostics")

st.markdown(
    """
    <div style="color: white; filter: brightness(150%);">
        In the realm of medical diagnostics, the development of an advanced brain tumor identification model stands as a testament to the potential of artificial intelligence in healthcare.<br>
        Spearheaded by <b>Aswin Damarapalli</b>, this model leverages the power of AI to analyze medical imaging data and provide valuable insights into the presence and characteristics of brain tumors.
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("Model Highlights:")
st.markdown(
    """
    <div style="color: white; filter: brightness(150%);">
        1. <b>Image Recognition:</b> The model excels in accurately identifying and categorizing brain tumors in various medical imaging modalities, including MRI and CT scans.<br>
        2. <b>Predictive Analytics:</b> By employing predictive analytics, the model can forecast the growth patterns and potential risks associated with detected tumors.<br>
        3. <b>Collaborative Approach:</b> <b>Aswin Damarapalli</b> has collaborated with medical professionals to ensure the model aligns with the highest standards of accuracy and reliability.
    </div>
    """,
    unsafe_allow_html=True
)

# Chatbot Section
st.title("Chatbot for Medical Assistance: Enhancing Patient Support")

st.markdown(
    """
    <div style="color: white; filter: brightness(150%);">
        Complementing the brain tumor identification model, <b>Aswin Damarapalli</b> has developed an intelligent chatbot aimed at providing assistance and information to individuals seeking insights into medical conditions, treatments, and general healthcare inquiries.
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("Chatbot Features:")
st.markdown(
    """
    <div style="color: white; filter: brightness(150%);">
        1. <b>Natural Language Processing:</b> The chatbot employs advanced natural language processing (NLP) techniques
         to understand and respond to user queries in a conversational manner.<br>
        2. <b>Medical Information:</b> Users can access accurate and up-to-date medical information, making the chatbot 
        a valuable resource for health-related questions.<br>
        3. <b>Empathy and Support:</b> Designed with a human touch, the chatbot aims to provide empathy and support to 
        users navigating health concerns.
    </div>
    """,
    unsafe_allow_html=True
)

# Footer with disclaimer
st.markdown(
    """
    ---
    #### About the Author:
    Model Developed by: <b>Aswin Damarapalli</b>.

    I'm Damarapalli Aswin, a dedicated Data Scientist deeply passionate about the realms of AI and Machine Learning.
    With a robust background in Information Technology, specifically in the domain of AI, I've had the privilege of 
    accumulating valuable experience and contributing meaningfully to the field. I hope it sparks insightful 
    conversations among our community of readers.<br>

    <b>Connect:</b><br>
    **LinkedIn**: [Aswin Damarapalli](https://www.linkedin.com/in/aswin-kumar-damarapalli/)<br>
    **Email**: [aswindk.aiml@gmail.com](mailto:aswindk.aiml@gmail.com)
    """,
    unsafe_allow_html=True
)

# Footer with disclaimer
st.markdown(
    """
    ---
    #### Disclaimer:
    The predictions made by the AI model are for demonstration purposes only and should not be considered as definitive 
    truths. Always consult with a qualified professional for accurate information.  
    """
)
