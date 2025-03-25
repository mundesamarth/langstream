import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
import urllib
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("LANGCHAIN_API_KEY")
base_url = os.getenv("BASE_URL")

# Initialize session state for chat history if not already done
if "messages" not in st.session_state:
    st.session_state.messages = []  # Stores the conversation history
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

# Initialize the model
llm = ChatOpenAI(
    base_url=base_url,
    api_key= api_key,
    model="meta-llama/llama-3.1-70b-instruct:free",
)

# Define prompt template
prompt = PromptTemplate(
    input_variables=["history", "input"],
    template="""
    You are a helpful chatbot. Here is the conversation so far:
    {history}
    Human: {input}
    AI:
    """
)

# Create LLM Chain with memory
conversation = LLMChain(llm=llm, prompt=prompt, memory=st.session_state.memory)

# Streamlit UI
st.title("Chatbot with Memory")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    response = conversation.run(user_input)

    # Save response in memory
    st.session_state.memory.save_context({"input": user_input}, {"output": response})

    # Display AI response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

print("Password/Enpoint IP for localtunnel is:",urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip("\n"))

