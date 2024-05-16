# Reminisc

Reminisc is an OpenAI inspired open-source memory framework for LLMs.

![demo](demo.gif)

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
CHROMA_INDEX_NAME=reminisc-memories
```

## Usage

To start the Reminisc chat assistant, run:

```bash
streamlit run app.py
```

You can now interact with the assistant by entering your messages. The assistant will generate responses based on the stored memories and the current conversation context.

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
    - `vectordb.py`: Interacts with the Chroma vector database for memory storage and retrieval.
    - `memory/`: Contains memory-related modules.
      - `creator.py`: Creates memories from user input using OpenAI's language model.
      - `manager.py`: Manages the storage and retrieval of memories using the vector database.
- `requirements.txt`: Lists the required Python dependencies.
- `.env.example`: An example environment file template.
- `app.py`: The Streamlit app for demo purposes.

## Contributing

We welcome contributions to improve Reminisc and expand its capabilities. Please open an issue for suggestions or bug reports, or submit a pull request for code contributions.

Priority areas for contributions:

- Packaging: Convert this framework into a distributable Python package.
- LLM Integrations: Integrate additional language models for generating responses.
- Vector Database Support: Expand support for various vector databases for memory storage and retrieval.
- User-Controlled Memory: Allow users to instruct the assistant to remember or forget information and manage memories.
- Memory Consolidation and Updating: Implement mechanisms for consolidating and updating memories to improve response relevance and coherence.

## License

This project is licensed under the [Apache License](LICENSE).
