# Reminisc API Documentation

This document provides an overview of the API routes available in the Reminisc memory framework.

## Base URL

The base URL for all API routes is:

```
http://localhost:8000/v0/memory
```

## API Routes

### Create Memory

- **URL**: `/`
- **Method**: `POST`
- **Request Body**:
  - `content` (string): The content of the memory to be created.
  - `user_id` (string): The ID of the user associated with the memory.
- **Response**:
  - `content` (string): The content of the created memory.
  - `metadata` (object): Additional metadata associated with the memory, including the `user_id`.
- **Description**: Creates a new memory with the provided content for the specified user.

### Get All Memories

- **URL**: `/`
- **Method**: `GET`
- **Query Parameters**:
  - `user_id` (string): The ID of the user to retrieve memories for.
- **Response**:
  - An array of memory objects, each containing:
    - `content` (string): The content of the memory.
    - `metadata` (object): Additional metadata associated with the memory, including the `user_id`.
- **Description**: Retrieves all stored memories for the specified user.

### Delete Memory

- **URL**: `/{memory_id}`
- **Method**: `DELETE`
- **URL Parameters**:
  - `memory_id` (string): The ID of the memory to be deleted.
- **Query Parameters**:
  - `user_id` (string): The ID of the user associated with the memory.
- **Response**:
  - `message` (string): A success message indicating that the memory was deleted.
- **Description**: Deletes a memory with the specified ID for the specified user.

### Search Memories

- **URL**: `/search`
- **Method**: `POST`
- **Request Body**:
  - `query` (string): The search query to find relevant memories.
  - `user_id` (string): The ID of the user to search memories for.
- **Response**:
  - An array of memory objects that match the search query, each containing:
    - `content` (string): The content of the memory.
    - `metadata` (object): Additional metadata associated with the memory, including the `user_id`.
- **Description**: Searches for memories based on the provided query for the specified user and returns relevant results.

### Classify Input

- **URL**: `/classify`
- **Method**: `POST`
- **Request Body**:
  - `query` (string): The user input to be classified.
  - `user_id` (string): The ID of the user associated with the input.
- **Response**:
  - `should_store_memory` (boolean): Indicates whether the input should be stored as a memory.
- **Description**: Classifies the user input to determine if it should be stored as a memory for the specified user.

### Process User Input

- **URL**: `/process`
- **Method**: `POST`
- **Request Body**:
  - `query` (string): The user input to be processed.
  - `user_id` (string): The ID of the user associated with the input.
- **Response**:
  - `content` (string): The content of the processed memory.
  - `metadata` (object): Additional metadata associated with the memory, including the `user_id`.
- **Description**: Processes the user input, creates a memory if necessary, and returns the processed memory for the specified user.
