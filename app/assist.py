import st_pages
import streamlit as st
import google.generativeai as genai
import base64

# ------------------ Session State Initialization ------------------
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'previous_input' not in st.session_state:
    st.session_state.previous_input = ''
if 'input_query' not in st.session_state:
    st.session_state.input_query = ''
if 'send_triggered' not in st.session_state:
    st.session_state.send_triggered = False

# ------------------ Main App ------------------
def code():
    # Configure Google Gemini
    api_key = 'AIzaSyCBr_TtY7MksHOEYRd38kD-hmqIKS25RvM'
    genai.configure(api_key=api_key)

    # Background image setup
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

    # Initialize Gemini model
    model = genai.GenerativeModel('gemini-2.5-flash')  # Ensure it's multimodal
    chat = model.start_chat(history=[])

    # File uploader
    uploaded_image = st.file_uploader("Upload an X-ray or MRI image (optional)", type=['png', 'jpg', 'jpeg'])

    # -------- Get response from Gemini -------------
    def get_response(prompt, image_file=None):
        input_prompt = """
        You are a polite and helpful AI assistant specializing in brain tumor analysis.
        - If the question is about brain tumors, answer thoroughly, clearly, and helpfully.
        - If it is about another medical topic (not brain-related), politely explain that you are trained only in brain tumor topics and cannot answer that question.
        - If it is not medical at all, politely say you do not have information on that topic.
        - If an image is uploaded, analyze it and include relevant insights if possible.
        - If asked about your model or structure, reply: "I’m a custom AI model trained on 25,000+ X-ray and MRI images using Google AI Studio. My development, training, and deployment were handled by Aswin."
        """

        if image_file:
            image_data = image_file.read()
            image_parts = [{"mime_type": image_file.type, "data": image_data}]
            response = chat.send_message([input_prompt, prompt], image_parts=image_parts)
        else:
            response = chat.send_message([input_prompt, prompt])
        return response

    # -------- Flag setter for send button / Enter key -------------
    def flag_send_message():
        st.session_state.send_triggered = True

    # -------- Send message logic -------------
    def send_message():
        query = st.session_state.input_query.strip()
        if query:
            response = get_response(query, image_file=uploaded_image)
            st.session_state.chat_history.append(('User', query))
            st.session_state.previous_input = ''
            st.session_state.input_query = ''

            for chunk in response:
                st.session_state.chat_history.append(('Bot', chunk.text))

    # --------- UI Layout ---------------
    st.header('Health Assistant 💬')
    st.subheader('I am an AI assistant here to help you with questions about brain tumors.')

    # Input box with Enter key support
    st.text_input(
        'Please Enter your query here',
        key='input_query',
        value=st.session_state.get('previous_input', ''),
        on_change=flag_send_message,
    )

    # Send button
    st.button("Send", on_click=flag_send_message)

    # Trigger message sending only once
    if st.session_state.send_triggered:
        send_message()
        st.session_state.send_triggered = False

    # Display chat history
    for sender, message in st.session_state.chat_history:
        color = "white" if sender == "User" else "grey"
        st.markdown(f'<div style="color: {color};"><b>{sender}:</b> {message}</div>', unsafe_allow_html=True)

    # Sidebar with usage instructions
    st.sidebar.title("Welcome to the Brain Tumor Health Assistant!")
    st.sidebar.subheader('Instructions')
    st.sidebar.write("📤 **Upload Image (optional):** Upload an X-ray or MRI scan.")
    st.sidebar.write("💬 **Input Query:** Ask brain tumor-related questions.")
    st.sidebar.write("⏎ Press **Enter** or click **Send** to ask your question.")
    st.sidebar.write("🕒 **Chat History:** Your conversation appears in the main area.")

# ------------------ Run App ------------------
if __name__ == "__main__":
    code()
