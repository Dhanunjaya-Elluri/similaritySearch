# nexMart-CodeChallenge (Work in Progress)

## Description

This is a code challenge from NexMart. The task is to deploy an ML model as a REST API in a containerized service with a CI/CD setup. The model is a Sentence Transformer (SBERT) designed to compare product descriptions with any given set of queries, e.g., to find similar products and return the most suitable product descriptions.

Tech Stack used:

- [Python (3.12)](https://www.python.org/downloads/release/python-3120/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)
- [GitHub (CI/CD)](https://github.com/)

## Project Structure

- `src/nexmart`: The main application code.
- `tests`: Unit and integration tests.
- `pyproject.toml`: The project configuration file.
- `README.md`: This file.
- `Dockerfile`: The Dockerfile for the containerized service.

## Project Setup (To run the project locally)

1. Clone the repository. Make sure you have [Git](https://git-scm.com/downloads) installed.

   ```bash
   $ git clone https://github.com/Dhanunjaya-Elluri/nexMart-CodeChallenge.git
   ```

2. Install the dependencies using `uv`.

    - For this project, I used `uv` to manage the dependencies.
    To install `uv`, and dependencies, follow the steps below:

        ```bash
        $ curl -LsSf https://astral.sh/uv/install.sh | sh
        ```

    - Create a virtual environment and install the dependencies:

        ```bash
        $ uv venv -p 3.12 --seed
        ```

    - Activate the virtual environment:
        - For Windows:
            ```bash
            $ .venv\Scripts\activate
            ```
        - For Linux / MacOS:
            ```bash
            $ source .venv/bin/activate
            ```
    - Install the dependencies:
        ```bash
        $ uv pip install -e .
        ```

3. Run the FastAPI server:

    ```bash
    $ uvicorn src.nexmart.main:app --reload
    ```
    The server will be running on [http://localhost:8000](http://localhost:8000).

    - Test the health endpoint:
        ```bash
        $ curl http://localhost:8000/api/v1/health
        ```
        Response:
        ```json
        {
            "status": "healthy"
        }
        ```

    - Test the similarity endpoint:
        ```bash
        $ curl -X POST http://localhost:8000/api/v1/similarity \
            -H "Content-Type: application/json" \
            -d '{
                "text": ["What can I use to cut wood?"],
                "products": [
                    "High-performance circular saw with laser guide for accurate cuts.",
                    "Heavy-duty claw hammer with a non-slip grip handle for precise strikes.",
                    "Durable 25ft tape measure with easy-lock and belt clip.",
                    "High-torque ratchet screwdriver for efficient screwdriving."
            ],
            "top_k": 2
            }'
        ```
        Response:
        ```json
        {
            "query": "What can I use to cut wood?",
            "matches": [
            {
                "product": "High-performance circular saw with laser guide for accurate cuts.",
                "score": 0.8923
            },
            {
                "product": "Heavy-duty claw hammer with a non-slip grip handle for precise strikes.",
                "score": 0.8565
                }
            ]
        }
        ```
    - Swagger UI:
        - http://localhost:8000/docs
        - http://localhost:8000/redoc
        - http://localhost:8000/openapi.json


4. Running the tests:
    - Install the dev and test dependencies:
        ```bash
        $ uv pip install -e ".[test,dev]"
        ```
    - Unit tests:
        ```bash
        $ pytest -v -m unit
        ```
    - Integration tests:
        ```bash
        $ pytest -v -m integration
        ```
    - To run all tests together:
        ```bash
        $ pytest -v
        ```

5. Run pre-commit hooks to check the code quality and format the code:
    - First install pre-commit:
        ```bash
        $ uv pip install pre-commit
        ```
    - Install pre-commit hooks:
        ```bash
        $ pre-commit install
        ```
    - Run pre-commit to check the code quality:
        ```bash
        $ pre-commit run --all-files
        ```

## Run using Docker

Make sure you have Docker installed on your machine.

- Build the Docker image:
    ```bash
    $ docker build -t nexmart-api:latest .
    ```
- Run the Docker image:
    ```bash
    $ docker run -d -p 8000:8000 nexmart-api:latest
    ```

Wait for the container to start and the FastAPI server to be running. You can test the endpoints as mentioned in the "Run the FastAPI server" section.
