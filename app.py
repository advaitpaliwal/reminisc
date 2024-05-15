from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from reminisc.src.memory.creator import MemoryCreator
from reminisc.src.memory.manager import MemoryManager
from reminisc.src.classifier import Classifier
import logging
import streamlit as st

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up the title and create instances of the required classes
st.set_page_config(page_title="Reminisc", layout="wide")
st.title("🧠 Reminisc")
st.info('Memory for conversational LLMs. https://github.com/advaitpaliwal/reminisc')
memory_creator = MemoryCreator()
memory_manager = MemoryManager()
classifier = Classifier()
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

chain = prompt_template | llm

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
    with chat_history_container:
        for message in st.session_state.messages:
            avatar = None
            if message["role"] == "assistant":
                avatar = "🧠"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # User input handling
    with input_container.container():
        prompt = st.chat_input("What is up?")

        if prompt:
            st.session_state.messages.append(
                {"role": "user", "content": prompt})
            with chat_history_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

            # Retrieve relevant memory based on user input
            relevant_memory = memory_manager.retrieve_memory(prompt)
            logger.debug(f"{relevant_memory=}")

            # Classify user input to determine if it should be stored as a memory
            should_store_memory = classifier.classify(prompt)
            logger.debug(f"{should_store_memory=}")

            if should_store_memory:
                # Store user input as a memory
                memory = memory_creator.create_memory(prompt)
                logger.debug(f"Memory created: {memory}")
                memory_manager.store_memory(memory)

            # Generate response using the LLM and conversation memory
            llm_input = {
                'retrieved_memory': relevant_memory,
                'input': prompt,
                'chat_history': conversation_memory.load_memory_variables({})[conversation_memory.memory_key]
            }
            stream = chain.stream(llm_input)

            with chat_history_container:
                if should_store_memory:
                    with st.expander("📝 Memory updated"):
                        st.write(memory)
                with st.chat_message("assistant", avatar="🧠"):
                    response = st.write_stream(stream)

            logger.info(f"User Input: {prompt}")
            logger.info(f"Generated Response: {response}")

            # Save the assistant's response in the session
            st.session_state.messages.append(
                {"role": "assistant", "content": response})

with memory_column:
    st.header("Memory Management")

    # Display all memories
    memories = memory_manager.memories
    for memory in memories:
        memory_id = memory["id"]
        timestamp = memory["timestamp"]
        memory_content = memory["memory"]

        with st.expander(f"{timestamp}"):
            st.write(f"**Memory ID:** {memory_id}")
            st.write(f"**Timestamp:** {timestamp}")
            st.write(f"**Memory:** {memory_content}")
            if st.button("Delete", key=memory_id):
                memory_manager.delete_memory(memory_id)
                st.experimental_rerun()

    with st.expander("✍️ Create New Memory"):
        new_memory = st.text_area("Enter a new memory")
        if st.button("Store Memory"):
            memory_manager.store_memory(new_memory)
            st.experimental_rerun()
