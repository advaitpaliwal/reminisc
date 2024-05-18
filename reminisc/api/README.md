# Reminisc API Documentation

This document provides an overview of the API routes available in the Reminisc memory framework.

## Base URL

The base URL for all API routes is:

```
http://localhost:8000/v0/memory
```

## Authentication

The API routes do not require authentication in the current implementation.

## Error Handling

If an error occurs during the processing of an API request, the API will return an appropriate HTTP status code along with an error message in the response body.

## API Routes

### Create Memory

- **URL**: `/`
- **Method**: `POST`
- **Request Body**:
  - `content` (string): The content of the memory to be created.
- **Response**:
  - `content` (string): The content of the created memory.
  - `metadata` (object): Additional metadata associated with the memory.
- **Description**: Creates a new memory with the provided content.

### Get All Memories

- **URL**: `/`
- **Method**: `GET`
- **Response**:
  - An array of memory objects, each containing:
    - `content` (string): The content of the memory.
    - `metadata` (object): Additional metadata associated with the memory.
- **Description**: Retrieves all stored memories.

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
- **Request Body**:
  - `query` (string): The search query to find relevant memories.
- **Response**:
  - An array of memory objects that match the search query, each containing:
    - `content` (string): The content of the memory.
    - `metadata` (object): Additional metadata associated with the memory.
- **Description**: Searches for memories based on the provided query and returns relevant results.

### Classify Input

- **URL**: `/classify`
- **Method**: `POST`
- **Request Body**:
  - `query` (string): The user input to be classified.
- **Response**:
  - `should_store_memory` (boolean): Indicates whether the input should be stored as a memory.
- **Description**: Classifies the user input to determine if it should be stored as a memory.

### Process User Input

- **URL**: `/process`
- **Method**: `POST`
- **Request Body**:
  - `query` (string): The user input to be processed.
- **Response**:
  - `content` (string): The content of the processed memory.
  - `metadata` (object): Additional metadata associated with the memory.
- **Description**: Processes the user input, creates a memory if necessary, and returns the processed memory.
