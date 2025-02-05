# Epam project
Project management/profiles dashboard - a service to create, update, share, and delete projects information (details, attached documents). 
User can create profile, create projects, and add documents inside the projects. 
Additionally, user of this project can grant roles, make changes, and according to added role, user can manage documents and projects.

## Technology used
- Python 3.10
- FastAPI
- PostgreSQL (with SQLAlchemy ORM)
- Docker
- CI/CD with GitHub Actions
- AWS S3 for file storage
- AWS Lambda for image processing

## Installation

  1. Clone the repository from GitHub:
    ```bash
       git clone https://github.com/brankadi/epam_project.git
       cd epam_project
  2. Set up a PostgreSQL database:
    1)	Ensure PostgreSQL is installed 
    2)	Run PostfreSQL inside Docker conteinter:
        Create .env file in root directory and change password with your own password to protect database:
        DATABASE_URL=postgresql://postgres:<your-password>@localhost:5432/mydatabase
  3. Run the Docker - docker-compose.yml:
    docker-compose up --build

## Usage

This API allows for user registration, login and managing projects and documents inside of projects.
Below are the available endpoints for interacting with the application.

    1.	Register User (POST/auth) 
        -	Register new user
        -	Request body (JSON): 
          { 
          "username": "newuser", 
          "password": "password123", 
          "name": "Super",
          "surname": "Mario",
          "email": supermario@example.com
           }
          -	Response (JSON):
          {
          “id”: 1,
          "username": "newuser", 
          "name": "Super",
          "surname": "Mario",
          "email": supermario@example.com
           }
    
    
    2.	Login (POST/token)
        -	Login and generate JWT token
        -	Request body: 
          username: newuser 
          password: password123
          -	Response (JSON):
          { 
          "access_token": "your_generated_token_here",
           "token_type": "bearer"
           }
    
    
    3.	Create Project (POST/projects)
        -	Create new Project. User that creates new project is admin.
        -	Request body (JSON):
          {
          "name": "New Project",
          "description": "Description of the project", 
          "owner_id": 1 
          }
          -	Response (JSON):
          { 
          "id": 1, 
          "name": "New Project", 
          "description": "Description of the project", 
          "owner_id": 1 
          }
    4.	Get all Projects (GET/projects)
        - Get list of all projects that have already been created.
        -	Response (JSON):
                  [ 
                     { 
          "id": 1, 
          "name": "New Project",
          "description": "Description of the project", 
          "owner_id": 1 
                     }, 
                     { 
          "id": 2, 
          "name": "Another Project", 
          "description": "Another project description", 
          "owner_id": 2
                      }
                   ]
          
    5.	Get Project info (GET/projects/{project_id}/info)
        -	Get information about specific project 
        -	Requested parameter: project_id (integer)
        -	Response (JSON):
        {
          "id": 1,
          "name": "New Project",
          "description": "Description of the project",
          "owner_id": 1
        }
        
        
    6.	Update Project (PUT/projects/{project_id}/inf)
        -	Update project information.
        -	Requested parameter: project_id (integer)
        -	Requested body (JSON):
        { 
        "name": "Updated Project", 
        "description": 
        "Updated project description", 
        "owner_id": 1 
        }
        -	Response (JSON):
        {
          "id": 1,
          "name": "Updated Project",
          "description": "Updated project description",
          "owner_id": 1
          "modified_by": username
        }
        
    7.	Delete Project (DELETE/projects/{project_id})
        -	Delete a project by ID. Just admin of the project can delete project.
        -	Parameter requester: project_id (integer)
        -	Response (JSON):
        {
        “messege”: “Project {project_id} deleted”
        }
    
      




