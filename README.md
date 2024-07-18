# Inventory Service

This is a simple inventory management service written in Python using FastAPI. 

## Features
- Add a single item to a user's inventory
- Add multiple items to a user's inventory
- Fetch a user's inventory
- Subtract from a user's inventory

## Setup

### Requirements
- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite (default, can change to another DB if needed)

### Installation
1. Clone the repository:
    ```
    git clone https://github.com/sydneybojsza/inventory_service.git
    cd inventory_service
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Setup the database
    ```bash
    python setup.py setup_db
    ```

5. Populate the database
    ```bash
    python setup.py populate_db
    ```

6. Run the service:
    ```bash
    python bin/run.py # On Windows use `python .\bin\run.py`
    ```

7. The service will be available at `http://127.0.0.1:8000`.

## Usage

- Use an API client like Postman or cURL to interact with the endpoints.
- Use the `/token` endpoint to get a bearer token for authentication.
- When consuming via the swagger `/docs` endpoint, authorize against all endpoints with the `Authorize` button on the top-right corner

### Test Logins

| User      | Password  |
| --------- | --------- |
| testuser1 | password1 |
| testuser2 | password2 |


## Endpoints

- `POST /inventory/add_item/`: Add a single item to the inventory.
- `POST /inventory/add_items/`: Add multiple items to the inventory.
- `GET /inventory/`: Fetch the user's inventory.
- `POST /inventory/subtract_item/`: Subtract an item from the inventory.

## Running Tests
A simple CICD pipeline which builds the app, runs a linter and runs unit tests has been created in `.github/python-app.yml`

To run the tests locally:
    ```
    python setup.py test
    ```
