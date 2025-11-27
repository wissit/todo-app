# Django TODO App

A comprehensive TODO application built with Django and Python, featuring a modern UI with Tailwind CSS and user authentication.

## Features

-   **User Authentication**: Register, login, and logout functionality.
-   **Data Isolation**: Each user has their own private list of TODOs.
-   **CRUD Operations**: Create, Read, Update, and Delete TODOs.
-   **Due Dates**: Assign due dates to tasks using a calendar picker.
-   **Task Resolution**: Mark tasks as resolved/completed.
-   **Modern UI**: Clean, minimalist interface styled with Tailwind CSS.

## Setup

1.  **Install Dependencies**:
    This project uses `uv` for dependency management.
    ```bash
    uv sync
    ```

2.  **Run Migrations**:
    ```bash
    uv run python manage.py migrate
    ```

3.  **Run Development Server**:
    ```bash
    uv run python manage.py runserver
    ```

4.  **Access the App**:
    Open your browser and navigate to `http://127.0.0.1:8000/`.
