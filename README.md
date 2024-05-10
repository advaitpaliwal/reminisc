# Reminisc

Reminisc is an open-source memory for conversational LLMs.

## Features

- Stores user input as memories for future reference
- Retrieves relevant memories based on user queries
- Classifies user input to determine if it should be stored as a memory
- Generates contextual responses using retrieved memories and chat history
- Utilizes an LLM for memory creation and response generation
- Integrates with a vector database for efficient memory storage and retrieval

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/reminisc.git
cd reminisc
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

- Create a `.env` file in the project root directory.
- Add the following variables to the `.env` file:

```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_pinecone_index_name
```

## Usage

To start the Reminisc chat assistant, run the `chat.py` script:

```bash
python chat.py
```

You can now interact with the assistant by entering your messages. The assistant will generate responses based on the stored memories and the current conversation context.

To exit the chat, simply type `exit`.

## Configuration

You can modify the configuration settings in the `reminisc/config/config.py` file. The available settings include:

- `CLASSIFIER_MODEL_NAME`: The OpenAI model used for classifying user input (default: "gpt-3.5-turbo").
- `MEMORY_CREATOR_MODEL_NAME`: The OpenAI model used for creating memories from user input (default: "gpt-3.5-turbo").

## Project Structure

- `reminisc/`: The main package directory.
  - `config/`: Contains configuration files.
    - `config.py`: Defines the configuration settings for the project.
  - `src/`: Contains the core components of the Reminisc assistant.
    - `classifier.py`: Classifies user input to determine if it should be stored as a memory.
    - `memory/`: Contains memory-related modules.
      - `creator.py`: Creates memories from user input using OpenAI's language model.
      - `manager.py`: Manages the storage and retrieval of memories using the vector database.
    - `vectordb.py`: Interacts with the Pinecone vector database for memory storage and retrieval.
- `requirements.txt`: Lists the required Python dependencies.
- `.env.example`: An example environment file template.
- `chat.py`: The entry point for running the Reminisc chat assistant.

## Contributing

We welcome contributions to improve Reminisc and expand its capabilities. Please open an issue for suggestions or bug reports, or submit a pull request for code contributions.

Priority areas for contributions:

- LLM Integrations: Integrate additional language models for generating responses.
- Vector Database Support: Expand support for various vector databases for memory storage and retrieval.
- User-Controlled Memory: Allow users to instruct the assistant to remember or forget information and manage memories.
- Memory Consolidation and Updating: Implement mechanisms for consolidating and updating memories to improve response relevance and coherence.

## License

This project is licensed under the [Apache License](LICENSE).
