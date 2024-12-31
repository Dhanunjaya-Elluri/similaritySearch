# nexMart-CodeChallenge

[![Tests](https://github.com/Dhanunjaya-Elluri/nexMart-CodeChallenge/actions/workflows/run-tests.yml/badge.svg)](https://github.com/Dhanunjaya-Elluri/nexMart-CodeChallenge/actions/workflows/run-tests.yml)
[![Deploy](https://github.com/Dhanunjaya-Elluri/nexMart-CodeChallenge/actions/workflows/deploy.yml/badge.svg)](https://github.com/Dhanunjaya-Elluri/nexMart-CodeChallenge/actions/workflows/deploy.yml)

## Table of Contents

- [nexMart-CodeChallenge](#nexmart-codechallenge)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Project Structure](#project-structure)
  - [Project Setup - To run the project locally](#project-setup---to-run-the-project-locally)
  - [Run using Docker](#run-using-docker)
  - [CI/CD](#cicd)
    - [Continuous Integration (`run-tests.yml`)](#continuous-integration-run-testsyml)
    - [Continuous Deployment (deploy.yml)](#continuous-deployment-deployyml)
    - [Workflow Status](#workflow-status)
  - [Next Steps](#next-steps)
    - [1. Model Version Management](#1-model-version-management)
    - [2. Enhanced Monitoring](#2-enhanced-monitoring)
    - [3. Scalability Improvements](#3-scalability-improvements)
    - [4. Security Enhancements](#4-security-enhancements)
    - [5. Data Management](#5-data-management)
    - [6. Operational Features](#6-operational-features)

## Description

This is a code challenge from nexMart GmbH & Co. KG. The task is to deploy an ML model as a REST API in a containerized service with a CI/CD setup. The model is a Sentence Transformer (SBERT) designed to compare product descriptions with any given set of queries, e.g., to find similar products and return the most suitable product descriptions.

**Tech Stack used:**

- [Python (3.12)](https://www.python.org/downloads/release/python-3120/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)
- [GitHub (CI/CD)](https://github.com/)

> [!IMPORTANT]
> The monitoring strategy is available in the [monitoring/README.md](monitoring/README.md) file.

## Project Structure

- `src/nexmart`: The main application code.
- `monitoring/README.md`: The documentation for monitoring solutions.
- `tests`: Unit and integration tests.
- `pyproject.toml`: The project configuration file.
- `README.md`: This file.
- `Dockerfile`: The Dockerfile for the containerized service.

## Project Setup - To run the project locally

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
    - API Documentation:
        - http://localhost:8000/docs (Swagger UI)


4. Running the tests:
    - Install the test and lint dependencies:
        ```bash
        $ uv pip install -e ".[test,lint]"
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

Make sure you have Docker installed on your machine. On the root directory of this project, where the `Dockerfile` is located, run the following commands:

- Build the Docker image:
    ```bash
    $ docker build -t nexmart-api:latest .
    ```
- Run the Docker image:
    ```bash
    $ docker run -d -p 8000:8000 nexmart-api:latest
    ```

Wait for the container to start and the FastAPI server to be running. You can test the endpoints as mentioned in step 3 under [Project Setup - To run the project locally](#project-setup---to-run-the-project-locally).

## CI/CD

This project uses GitHub Actions for continuous integration and deployment. The workflow is split into two parts:

### Continuous Integration (`run-tests.yml`)

The CI pipeline runs on every push and pull request to the master branch when changes are made to `src/` or `tests/` directories. It performs:

1. **Environment Setup**
   - Uses Python 3.12
   - Sets up `uv` for dependency management
   - Creates and activates a virtual environment

2. **Code Quality Checks**
   - Formatting check with `black`
   - Linting with `ruff`
   - Type checking with `mypy`

3. **Testing**
   - Runs unit tests (`pytest -v -m unit`)
   - Runs integration tests (`pytest -v -m integration`)
   - Enforces 90% code coverage threshold

### Continuous Deployment (deploy.yml)

This CD pipeline runs on every push to the master branch and on the successful completion of the CI pipeline. It:

1. **Build Stage**
   - Logs in to Docker Hub
   - Builds the Docker image
   - Tags the image with the commit SHA
   - Pushes the image to Docker Hub

2. **Security**
   - Uses Docker Hub secrets for authentication

### Workflow Status

You can check the status of the CI/CD pipelines:
- In GitHub Actions tab
- Through status badges in this README

The deployment is currently configured to push to Docker Hub. For production deployment, additional stages can be added to deploy to cloud platforms like AWS, GCP, or Azure.

## Next Steps

To evolve this into a full-scale production system, the following enhancements could be implemented:

### 1. Model Version Management
- Implement a model registry service to manage different versions of models. We can use `mlflow` to manage the models.
- Add version tracking with metadata (training date, performance metrics, dataset version).
- Support A/B testing between model versions before publishing the new version to production.
- Enable automated model validation before deployment.
- Implement rollback mechanisms for model versions.
- Store model artifacts in cloud storage (e.g. S3).

### 2. Enhanced Monitoring
- As described in the [monitoring/README.md](monitoring/README.md) file.

### 3. Scalability Improvements
- Add caching layer for frequently accessed embeddings.
- Implement batch processing for large query sets.
- Enable auto-scaling based on traffic patterns or resource utilization.

### 4. Security Enhancements
- Add authentication and authorization to the API.
- Implement rate limiting.
- Add request validation and sanitization.
- Enable audit logging.
- Implement secure package updates. Always install the dependencies from the trusted source.

### 5. Data Management
- Add product catalog versioning.
- Implement embedding database for faster lookups.
- Add data validation pipelines.
- Enable periodic model retraining.
- Implement data retention policies.

### 6. Operational Features
- The current deployment just builds the docker image and pushes it to the container registry. Implement a CI/CD pipeline to automate the deployment depending on where we want to deploy the API.
- Conduct stress testing to ensure the API can handle high traffic and load.
- Enable automated backups.
- Implement disaster recovery procedures.

These enhancements would make this application more robust, maintainable, and suitable for production use at scale.
