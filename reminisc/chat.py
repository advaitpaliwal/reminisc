from langchain_openai import ChatOpenAI
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from reminisc.src.memory.manager import MemoryManager
from reminisc.src.classifier import Classifier
import logging

logger = logging.getLogger(__name__)


class LangChainChat:
    def __init__(self):
        self.memory_manager = MemoryManager()
        self.classifier = Classifier()
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=7
        )
        self.prompt = PromptTemplate(
            input_variables=["retrieved_memory",
                             "chat_history", "human_input"],
            template=(
                "System: You are an AI assistant with access to two types of memory:\n"
                "1. Retrieved Memory: This is your own memory that you can use to provide information and context relevant to the conversation.\n"
                "2. Chat History: This is the history of the current conversation, limited to the last 7 messages.\n\n"
                "Use the retrieved memory and chat history to generate a relevant and contextual response to the user's input.\n\n"
                "Retrieved Memory: {retrieved_memory}\n\n"
                "Chat History: {chat_history}\n\n"
                "Human: {human_input}\n"
                "Assistant:"
            ),
        )
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt,
            verbose=True,
            input_key="human_input",
            memory_variables=["chat_history",
                              "retrieved_memory"]
        )

    def process_message(self, user_input):
        # Retrieve relevant memory based on user input
        relevant_memory = self.memory_manager.retrieve_memory(user_input)

        # Classify user input to determine if it should be stored as a memory
        should_store_memory = self.classifier.classify(user_input)
        if should_store_memory:
            # Store user input as a memory
            self.memory_manager.store_memory(user_input)

        # Generate response
        response = self.conversation.predict(
            human_input=user_input,
            retrieved_memory=relevant_memory
        )

        logger.info(f"User Input: {user_input}")
        logger.info(f"Generated Response: {response}")

        return response


# Example usage
if __name__ == "__main__":
    chat = LangChainChat()
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            break
        response = chat.process_message(user_input)
        print(f"Assistant: {response}")
