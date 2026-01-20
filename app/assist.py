import st_pages
import streamlit as st
import google.generativeai as genai
import base64
import os

api_key=os.getenv("genai_api_key")
if not api_key:
    api_key='AIzaSyDkiTgRsP3BWPOlXW93lBY7a17noBy-RZk'

def code():
    genai.configure(api_key=api_key)

    # Background image
    image_path = "app/Chatbot.png"
    image_data = open(image_path, "rb").read()
    image_base64 = base64.b64encode(image_data).decode()

    st.markdown(
        f"""
            <style>
                .stApp {{
                    background-image: url('data:image/png;base64,{image_base64}');
                    background-size: cover;
                    background-repeat: no-repeat;
                    opacity: 0.6
                }}
            </style>
            """,
        unsafe_allow_html=True
    )

    model = genai.GenerativeModel('gemini-2.0-flash')
    chat = model.start_chat(history=[])

    # Session states
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'previous_input' not in st.session_state:
        st.session_state['previous_input'] = ''

    def get_response(prompt):
        input_prompt = """
        You are a polite and helpful AI assistant specializing in brain tumor analysis.
        - If the question is about brain tumors, answer thoroughly, clearly, and helpfully.
        - If it is about another medical topic (not brain-related), politely explain that you are trained only in brain tumor topics and cannot answer that question.
        - If it is not medical at all, politely say you do not have information on that topic.
        - If the user asks about your model type, internal structure, how you were trained, or who built you, respond with the following:

            "I’m a custom AI model trained on 25,000+ X-ray and MRI images using Google AI Studio. My development, training, and deployment were handled by Aswin."
        - If anyone ask who is Aswin, simply answer the developer behind you to train on brain tumor images.
        """
        response = chat.send_message([input_prompt, prompt])
        return response

    # App UI
    st.header('Health Assistant 💬')
    st.subheader('I am an AI assistant here to help you with questions about brain tumors.')

    # Chat input box
    input_text = st.text_input(
        'Please Enter your query here',
        key='input_query',
        value=st.session_state.get('previous_input', ''),
        on_change=lambda: send_message(),  # Trigger on pressing Enter
    )

    def send_message():
        query = st.session_state.input_query.strip()
        if query:
            response = get_response(query)
            st.session_state.chat_history.append(('User', query))
            st.session_state.previous_input = ''  
            st.session_state.input_query = ''  # Clear the text box immediately

            for chunk in response:
                st.session_state.chat_history.append(('Bot', chunk.text))

    # Display chat history
    for sender, message in st.session_state.chat_history:
        color = "white" if sender == "User" else "grey"
        st.markdown(f'<div style="color: {color};"><b>{sender}:</b> {message}</div>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("Welcome to the Brain Tumor Health Assistant!")
    st.sidebar.subheader('Instructions')
    st.sidebar.write("**Input Query:** Enter your brain tumor-related queries in the text box at the bottom of the page.")
    st.sidebar.write('Press **Enter** or click the button to submit your question.')
    st.sidebar.write('**Chat History:** Your conversation history will be displayed above.')

if __name__ == "__main__":
    code()
