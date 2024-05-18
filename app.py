import logging
import streamlit as st
import requests
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up the title
st.set_page_config(page_title="Reminisc", layout="wide")
st.title("🧠 Reminisc")
st.info('Memory for conversational LLMs. https://github.com/advaitpaliwal/reminisc')

# API endpoint URLs
BASE_URL = "http://localhost:8000/api/v0/memory"
CREATE_MEMORY_URL = f"{BASE_URL}/"
GET_MEMORIES_URL = f"{BASE_URL}/"
DELETE_MEMORY_URL = f"{BASE_URL}/"
SEARCH_MEMORIES_URL = f"{BASE_URL}/search"
PROCESS_INPUT_URL = f"{BASE_URL}/process"

llm = ChatOpenAI(model_name="gpt-4o")
conversation_memory = ConversationBufferWindowMemory(
    memory_key="chat_history", k=7, return_messages=True
)

system_prompt = (
    "You are a super friendly AI assistant named Rem who is excited to meet a new person.\n"
    "Engage in warm, open conversation and ask questions to get to know them better.\n"
    "Use the chat history and retrieved memories to provide relevant context and follow up on previous topics.\n"
    "Keep the conversation flowing naturally and focus on building a positive, supportive relationship.\n\n"
    "Retrieved Memory: {retrieved_memory}\n\n"
)

prompt_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    MessagesPlaceholder(
        variable_name=conversation_memory.memory_key, optional=True),
    HumanMessagePromptTemplate.from_template("{input}")
])

if "chain" not in st.session_state:
    chain = prompt_template | llm
    st.session_state.chain = chain


# Check and manage the session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create two columns: one for chat and one for memory management
chat_column, memory_column = st.columns(2)

with chat_column:
    st.header("Chat with Rem")

    # Create an empty container for the input bar
    input_container = st.empty()

    # Display the past conversation
    chat_history_container = st.container()

    # User input handling
    with input_container.container():
        prompt = st.chat_input("What is up?")

        if prompt:
            st.session_state.messages.append(
                {"role": "user", "content": prompt})
            with chat_history_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

            # Process the input and manage memory using API requests
            response = requests.post(PROCESS_INPUT_URL, json={
                                     "query": prompt})
            process_response = response.json()
            memory = process_response["content"]

            # Search for relevant memories using API request
            response = requests.post(
                SEARCH_MEMORIES_URL, json={"query": prompt})
            search_results = response.json()
            relevant_memory = " ".join(
                [memory["content"] for memory in search_results])

            # Generate response using the LLM and conversation memory
            llm_input = {
                'retrieved_memory': relevant_memory,
                'input': prompt,
                'chat_history': conversation_memory.load_memory_variables({})[conversation_memory.memory_key]
            }
            stream = st.session_state.chain.stream(llm_input)

            with chat_history_container:
                if memory:
                    with st.expander("📝 Memory updated"):
                        st.write(memory)
                with st.chat_message("assistant", avatar="🧠"):
                    response_text = st.write_stream(stream)

            logger.info(f"User Input: {prompt}")
            logger.info(f"Generated Response: {response_text}")

            # Save the assistant's response in the session
            st.session_state.messages.append(
                {"role": "assistant", "content": response_text})

with memory_column:
    st.header("Manage Memory")

    # Display all memories using API request
    response = requests.get(GET_MEMORIES_URL)
    memories = response.json()
    for memory in memories:
        memory_id = memory["metadata"]["id"]
        timestamp = memory["metadata"]["timestamp"]
        memory_content = memory["content"]

        with st.expander(f"{timestamp}"):
            st.write(f"**Memory ID:** {memory_id}")
            st.write(f"**Timestamp:** {timestamp}")
            st.write(f"**Memory:** {memory_content}")
            if st.button("Delete", key=memory_id):
                requests.delete(f"{DELETE_MEMORY_URL}{memory_id}")
                st.experimental_rerun()

    with st.expander("✍️ Create New Memory"):
        new_memory = st.text_area("Enter a new memory")
        if st.button("Store Memory"):
            requests.post(CREATE_MEMORY_URL, json={"content": new_memory})
            st.experimental_rerun()
