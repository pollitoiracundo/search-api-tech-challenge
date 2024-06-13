# Search NPI using noise data and GPT4o

This is a simple FastAPI + React project that allows users to search for health professionals and clinics. The application includes a search bar for inputting queries and displays the search results in a card format similar to Google Search results. The goal is to handle `POST` requests on the `/search/doctors` endpoint in AWS.

## Features

- Search for health professionals and clinics using a query input.
- Display results in a card format with details such as NPI, name, primary practice address, phone, and primary taxonomy.
- Sort results based on a normalized score on a 1-10 scale.
- Disable the search button while waiting for the API response.
- Show a message when no results are found.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Node.js
- npm (Node Package Manager)

## Installation

1. **Clone the repository**:
    ```bash
    git clone <this repo>
    cd <this repo folder>
    ```

2. **Create a virtual environment**:
    ```bash
    cd backend
    python -m venv backend_venv
    source backend_venv/bin/activate  # On Windows use `venv\Scripts\activate`

    cd ../frontend
    npm install
    ```

## Running the Application

Run the application using Uvicorn:
```bash
uvicorn main:app --reload
```
```bash
npm start
```