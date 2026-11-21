# TaskFlow

TaskFlow is a task management REST API built with **FastAPI** and **PostgreSQL**.

It allows users to manage projects and tasks through a RESTful API, with authentication and ownership-based access control.

## Features

- User registration and login.
- Secure password hashing.
- JWT-based authentication.
- Create, retrieve, update, and delete projects.
- Create, retrieve, update, and delete tasks.
- Manage tasks within projects.
- Update task status and priority.
- Ownership-based access control to protect user data.
- RESTful API with FastAPI.

## Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy (Async ORM)
- Alembic (Database Migrations)
- Pydantic
- JWT (Authentication)
- Pytest (Testing)
- SQLite (Testing Database)

## Project Structure

```text
TaskFlow/
│
├── core/
│   └── security.py
│
├── migrations/
│
├── models/
│
├── routers/
│
├── schemas/
│
├── services/
│
├── tests/
│
├── database.py
├── dependencies.py
├── main.py
├── alembic.ini
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/YasharHosseinZadeh/TaskFlow.git
```

2. Navigate to the project directory:

```bash
cd TaskFlow
```

3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate the virtual environment:

**Linux / macOS:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory and configure the following variables:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

Replace the example values with your own PostgreSQL connection URL and a secure secret key.

## Database Migrations

Run the following command to apply database migrations:

```bash
alembic upgrade head
```

## Running the Application

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

After starting the application, visit:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Running Tests

Run the test suite using:

```bash
python -m pytest -v
```

## Author

**Yashar Hossein Zadeh**

- GitHub: [YasharHosseinZadeh](https://github.com/YasharHosseinZadeh)