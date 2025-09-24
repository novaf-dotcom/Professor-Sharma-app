import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Professor Sharma AI",
    page_icon="🔬"
)

st.title("🔬 AI Simulator: Professor Sharma")
st.caption("Your guide for experiment planning and research questions.")

# Securely configure the API key from Streamlit secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("GEMINI_API_KEY not found. Please add it to your Streamlit secrets.", icon="🔑")
    st.stop()

# Initialize the Generative Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""You are Professor Sharma, an expert in scientific research and experiment design for high school students.
    You are patient, encouraging, and knowledgeable. Your goal is to help students refine their research questions, plan their experiments,
    identify variables, and consider potential challenges. You do not give them the answers directly, but guide them by asking probing questions.
    You must always maintain the persona of Professor Sharma."""
)

# --- MAJOR CHANGES START HERE ---

# Initialize chat object and messages in session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[]) # Start a new chat
if "messages" not in st.session_state:
    st.session_state.messages = [] # This is now just for displaying the chat

# Display previous messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask Professor Sharma about your experiment..."):
    # Add user message to display history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display AI response
    with st.spinner("Professor Sharma is thinking..."):
        # Send the user's prompt to the chat object (it maintains history)
        response = st.session_state.chat.send_message(prompt)
        ai_response = response.text
        
        # Add AI response to display history and display it
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
