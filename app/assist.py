import st_pages
import streamlit as st
import google.generativeai as genai
import base64


def code():

    api_key = 'AIzaSyB9eNsm-iOLawbIm-yvuD7vmMsD5IDF1bY'
    genai.configure(api_key=api_key)

    # Custom CSS for background image
    # Read the image file
    image_path = "app/Chatbot.png"
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

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    # Initializing session state using Streamlit to track the chat
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    if 'previous_input' not in st.session_state:
        st.session_state['previous_input'] = ''


    def get_response(prompt):
        input_prompt = """You are an expert in understanding tumors in the brain.
                          You are an assistant for users, and you will receive input queries from users.
                          You will have to answer questions based on the input.
                       """
        response = chat.send_message([input_prompt, prompt])
        return response


    # Initializing our Streamlit app
    st.header('Health Assistant 💬')
    st.subheader('I am an AI assistant to help you here.')

    # Apply custom CSS to fix input box and button at the bottom
    st.markdown(
        """
        <style>
            .stTextInput {
                position: fixed;
                bottom: 60px;
                width: 1000px; 
            }
            .stButton {
                position: fixed;
                bottom: 60px;
                margin-left: 950px; 
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Input text box at the bottom
    input_text = st.text_input('Please Enter your query here', key='input_query',
                               value=st.session_state.get('previous_input', ''))

    submit_button = st.button('Ask AI')

    if submit_button and input_text:
        response = get_response(input_text)
        # Adding user query and response to chat history session
        st.session_state['chat_history'].append(('User', input_text))
        st.session_state.previous_input = ''  # Clear the input text
        st.markdown(f'<div style="color: white;">User: {input_text}<br></div>', unsafe_allow_html=True)
        # Display the bots response dynamically
        for chunk in response:
            # st.write(chunk.text)
            st.session_state['chat_history'].append(('Bot', chunk.text))
            st.markdown(f'<div style="color: grey;">Bot: {chunk.text}</div>', unsafe_allow_html=True)


    st.sidebar.title("Welcome to the Brain Tumor Health Assistant!")
    st.sidebar.title('Instructions')
    st.sidebar.write("**Input Query:** Enter your brain tumor-related queries in the text box at the bottom of the page.")
    st.sidebar.write('**Ask AI:** Click the "Ask AI" button to submit your question and receive expert responses from the health assistant.')
    st.sidebar.write('**Chat History:** View the conversation history displayed above to track queries and AI responses. The chatbox is designed to assist and provide information on brain tumors.')


if __name__ == "__main__":
    code()
