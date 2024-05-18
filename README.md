# Reminisc

Reminisc is an OpenAI inspired open-source memory framework for LLMs.

![demo](assets/demo.gif)

## Features

- Stores user input as memories for future reference
- Retrieves relevant memories based on user queries
- Classifies user input to determine if it should be stored as a memory
- Generates contextual responses using retrieved memories and chat history
- Utilizes an LLM for memory creation and response generation
- Integrates with Supabase and pgvector for efficient memory storage and retrieval

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
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## Supabase Setup

1. Initialize Supabase: Ensure you have the Supabase CLI installed. If not, install it by following the instructions [here](https://supabase.io/docs/guides/cli).

2. Apply database migrations: Reset the Supabase database and apply the migrations to set up the required tables and functions:

```bash
supabase db reset
```

This will execute the SQL files in the `supabase/migrations` directory, setting up the necessary database schema.

## Usage

To start Reminisc:

1. Run the FastAPI server:

```bash
fastapi dev main.py
```

2. In a separate terminal, run the Streamlit app:

```bash
streamlit run app.py
```

You can now interact with the assistant by entering your messages in the Streamlit app. The assistant will generate responses based on the stored memories and the current conversation context.

## API Documentation

For detailed information about the available API routes and their usage, please refer to the [documentation](reminisc/api/README.md).

## Configuration

You can modify the configuration settings in the `reminisc/config/config.py` file. The available settings include:

- `CLASSIFIER_MODEL_NAME`: The OpenAI model used for classifying user input (default: "gpt-3.5-turbo").
- `MEMORY_CREATOR_MODEL_NAME`: The OpenAI model used for creating memories from user input (default: "gpt-3.5-turbo").

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
