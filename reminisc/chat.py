from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from reminisc.src.memory.manager import MemoryManager
from reminisc.src.classifier import Classifier
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LangChainChat:
    def __init__(self):
        self.memory_manager = MemoryManager()
        self.classifier = Classifier()
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        self.conversation_memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=7,
            return_messages=True
        )
        self.system_prompt = (
                "You are a helpful AI assistant with access to memory:\n"
                "Retrieved Memory: This is your own memory that you can use to provide information and context relevant to the conversation.\n"
                "Use the retrieved memory and chat history to generate a relevant and contextual response to the user's input.\n\n"
                "Retrieved Memory: {retrieved_memory}\n\n"
        )
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_prompt),
            MessagesPlaceholder(variable_name=self.conversation_memory.memory_key, optional=True),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
        self.chain = self.prompt | self.llm

    def process_message(self, user_input):
        # Retrieve relevant memory based on user input
        relevant_memory = self.memory_manager.retrieve_memory(user_input)
        logger.debug(f"{relevant_memory=}")

        # Classify user input to determine if it should be stored as a memory
        should_store_memory = self.classifier.classify(user_input)
        logger.debug(f"{should_store_memory=}")
        if should_store_memory:
            # Store user input as a memory
            self.memory_manager.store_memory(user_input)

        # Generate response
        llm_input = {
            'retrieved_memory': relevant_memory,
            'input': user_input,
            'chat_history': self.conversation_memory.load_memory_variables({})[self.conversation_memory.memory_key]
        }

        
        response = self.chain.stream(llm_input)
        output = ""
        for chunk in response:
            yield chunk.content
            output += chunk.content

        self.conversation_memory.save_context({'input': user_input}, {'output': output})

        logger.info(f"User Input: {user_input}")
        logger.info(f"Generated Response: {response}")


# Example usage
if __name__ == "__main__":
    chat = LangChainChat()
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            break
        print(f"Assistant:", end="")
        for chunk in chat.process_message(user_input):
            print(chunk, end="", flush=True)
