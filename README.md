# EPAM Management Dashboard

Project management/profiles dashboard - a service to create, update, share, and delete projects information (details, attached documents). User can create profile, create projects, and add documents inside the projects. Additionally, user of this project can grant roles, make changes, and according to added role, user can manage documents and projects.

## Technology used

- Python 3.10
- FastAPI
- PostgreSQL (with SQLAlchemy ORM)
- Docker
- CI/CD with GitHub Actions

## Installation

1. Clone the repository from GitHub:
```bash
    git clone https://github.com/brankadi/epam_project.git
    cd epam_project
```
2. Set up a PostgreSQL database
    1. Ensure PostgreSQL is installed
    2. Run PostfreSQL inside Docker conteinter:
    - create .env file in root directory and change password with your own password to protect database:
    ``` 
    DATABASE_URL=postgresql://postgres:@localhost:5432/mydatabase
    ```
    3. Run the Docker:
    ```
    docker-compose up --build
    ```
    4. After usage you can stop the containers:
    ```
    docker-compose down
    ```

## Running the App

Adress for accessing the App:
```
http://localhost:8000
```
## Testing the App

- You can test the app in Swagger UI
```
http://localhost:8000/docs
```

## API Endpoints

This API allows for user registration, login and managing projects and documents inside of projects. 
Below are the available endpoints for interacting with the application.

1. Register User (POST/auth)
    - Register new user
    - If user exist: "Username already registered!"

2. User Login (POST/login)
    - Login and generate JWT token

3. Create new project (POST/project)
    - User that creates new project is 'admin'
    - If project already exist: "Project creation failed."

4. Get all projects (GET/projects)
    - Get list of all projects

5. Get project info (GET/projects/{project_id}/info)
    - Get information about specific project
    - If project doesn't exist: "Project {project_id} not found."

6. Update project (PUT/projects/{project_id}/info)
    - Update some or every information about project
    - If project doesn't exist: "Project {project_id} not found."

7. Delete project (DELETE/projects/{project_id})
    - Just the 'admin' of the project can delete the project
    - If the User is not 'admin' : "You are not authorized to delete this project"

8. Create documents (POST/documents)
    - Create document for some project

9. Get document info (GET/projects/{project_id}/documents)
    - Get information about document
    - If document doesn't exist: "Document not found."

10. Update the document (PUT/documents/{document_id})
    - Update some or every information about document
    - If document doesn't exist: "Document {document_id} not found."

