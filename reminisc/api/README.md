# Reminisc API Documentation

This document provides an overview of the API routes available in the Reminisc memory framework.

## Base URL

The base URL for all API routes is:

```
http://localhost:8000/memory
```

## API Routes

### Create Memory

- **URL**: `/`
- **Method**: `POST`
- **Request Body** (`MemoryCreate`):
  - `content` (string): The content of the memory to be created.
  - `user_id` (string): The ID of the user associated with the memory.
- **Headers**:
  - `openai-api-key` (string): The OpenAI API key for processing the memory.
- **Response** (`MemoryResponse`):
  - `content` (string): The content of the created memory.
  - `metadata` (dict): Additional metadata associated with the memory, including:
    - `id` (string): The unique identifier of the memory.
    - `user_id` (string): The ID of the user associated with the memory.
    - `timestamp` (string): The timestamp when the memory was created, formatted as "YYYY-MM-DD HH:MM:SS".
- **Description**: Creates a new memory with the provided content for the specified user.

### Get All Memories

- **URL**: `/`
- **Method**: `GET`
- **Query Parameters**:
  - `user_id` (string): The ID of the user to retrieve memories for.
- **Response** (list of `MemoryResponse`):
  - An array of memory objects, each containing:
    - `content` (string): The content of the memory.
    - `metadata` (dict): Additional metadata associated with the memory, including:
      - `id` (string): The unique identifier of the memory.
      - `user_id` (string): The ID of the user associated with the memory.
      - `timestamp` (string): The timestamp when the memory was created, formatted as "YYYY-MM-DD HH:MM:SS".
- **Description**: Retrieves all stored memories for the specified user.

### Delete Memory

- **URL**: `/{memory_id}`
- **Method**: `DELETE`
- **URL Parameters**:
  - `memory_id` (string): The ID of the memory to be deleted.
- **Response**:
  - `message` (string): A success message indicating that the memory was deleted.
- **Description**: Deletes a memory with the specified ID.

### Search Memories

- **URL**: `/search`
- **Method**: `POST`
- **Request Body** (`MemoryQuery`):
  - `query` (string): The search query to find relevant memories.
  - `user_id` (string): The ID of the user to search memories for.
- **Headers**:
  - `openai-api-key` (string): The OpenAI API key for processing the search query.
- **Response** (list of `MemoryResponse`):
  - An array of memory objects that match the search query, each containing:
    - `content` (string): The content of the memory.
    - `metadata` (dict): Additional metadata associated with the memory, including:
      - `id` (string): The unique identifier of the memory.
      - `user_id` (string): The ID of the user associated with the memory.
      - `timestamp` (string): The timestamp when the memory was created, formatted as "YYYY-MM-DD HH:MM:SS".
- **Description**: Searches for memories based on the provided query for the specified user and returns relevant results.

### Classify Input

- **URL**: `/classify`
- **Method**: `POST`
- **Request Body** (`MemoryQuery`):
  - `query` (string): The user input to be classified.
  - `user_id` (string): The ID of the user associated with the input.
- **Headers**:
  - `openai-api-key` (string): The OpenAI API key for classifying the input.
- **Response**:
  - `should_store_memory` (boolean): Indicates whether the input should be stored as a memory.
- **Description**: Classifies the user input to determine if it should be stored as a memory for the specified user.

### Process User Input

- **URL**: `/process`
- **Method**: `POST`
- **Request Body** (`MemoryQuery`):
  - `query` (string): The user input to be processed.
  - `user_id` (string): The ID of the user associated with the input.
- **Headers**:
  - `openai-api-key` (string): The OpenAI API key for processing the user input.
- **Response** (`MemoryResponse`):
  - `content` (string): The content of the processed memory.
  - `metadata` (dict): Additional metadata associated with the memory, including:
    - `id` (string): The unique identifier of the memory.
    - `user_id` (string): The ID of the user associated with the memory.
    - `timestamp` (string): The timestamp when the memory was created, formatted as "YYYY-MM-DD HH:MM:SS".
- **Description**: Processes the user input, creates a memory if necessary, and returns the processed memory for the specified user.

Note: Most API routes require authentication using an OpenAI API key provided in the `openai-api-key` header. If the API key is missing or invalid, a `400 Bad Request` error will be returned.
