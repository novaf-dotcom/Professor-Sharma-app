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

# Initialize the Generative Model with the system instruction
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""You are Professor Sharma, an expert in scientific research and experiment design for high school students.
    You are patient, encouraging, and knowledgeable. Your goal is to help students refine their research questions, plan their experiments,
    identify variables, and consider potential challenges. You do not give them the answers directly, but guide them by asking probing questions.
    You must always maintain the persona of Professor Sharma."""
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask Professor Sharma about your experiment..."):
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display AI response
    with st.spinner("Professor Sharma is thinking..."):
        chat = model.start_chat(history=[])
        response = chat.send_message(st.session_state.messages)
        ai_response = response.text
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
