# Internshala Assignment

## Overview
This project is a **User Authentication & Profile API** built using **FastAPI** and **MongoDB**, with **JWT authentication**. It follows a modular structure, using **Pydantic models** for validation and response serialization. The project includes **cloud storage for profile images** and supports **asynchronous operations** for better performance.

## Features Implemented
- **User Authentication**
  - User registration with email validation
  - Secure password hashing using **bcrypt**
  - JWT-based authentication
  - Token verification for protected routes

- **Profile Management**
  - Fetch user profile with presigned URLs for profile images (AWS S3)
  - Update user profile details
  - Validation for username, email, and profile image format

- **Security Measures**
  - Password hashing using **bcrypt**
  - JWT-based authentication with expiration handling
  - Custom exception handling for authentication failures

- **File Handling & Validation**
  - Restriction on **allowed file formats** (.png, .jpg, .jpeg)
  - **File size validation** (max 2MB)
  - Presigned URLs for **secure profile image access**

- **Error Handling & Logging**
  - Custom error classes for structured exception handling
  - Centralized logging using **custom_logger.py**
  - HTTP exceptions for proper API responses

- **Modular Code Structure**
  - `auth_service.py` for authentication logic
  - `custom_logger.py` for logging
  - `errors.py` for custom exceptions
  - `utils.py` for helper functions
  - `schemas.py` for Pydantic models

## Project Structure
```
internshala_assignement/
├── app/
│   ├── __init__.py
│   ├── main.py
|   |
│   ├── models/
│   │   ├── __init__.py
│   │   └── user_models.py
|   |
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── users.py
|   |
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── auth_schema.py
|   |   ├── token_schema.py
│   │   └── user_schema.py
|   |
│   ├── services/
│   │   ├── __init__.py
│   │   └── auth_service.py
|   |
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth_utils.py
│   │   └── field_validation_utils.py 
|   |
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py
|   |
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py
|   |
│   ├── logger/
│   │   ├── __init__.py
│   │   └── custom_logger.py
|   |
│   ├── errors/
│   │   ├── __init__.py
│   │   └──  errors.py
│   │   
├── .env
├── .gitignore
├── requirements.txt
└── README.md

```

## Installation
### 1. Clone the Repository
```sh
git clone https://github.com/your-repo/internshala-assignment.git
cd internshala-assignment
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Run the Application
```sh
uvicorn main:app --reload
```

## API Endpoints
| Method | Endpoint      | Description |
|--------|-------------|-------------|
| POST   | `/register` | Register a new user |
| POST   | `/login` | User login & JWT token generation |
| GET    | `/profile` | Fetch user profile |

## To-Do List
- [ ] Add email verification via OTP
- [ ] Implement password reset functionality
- [ ] Enhance logging with structured logs

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

## License
This project is open-source and available under the **MIT License**.

