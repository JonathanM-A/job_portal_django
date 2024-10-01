
# Django Job Portal API

### Overview
This project is a **Job Portal API** built with **Django** and **Django REST Framework**. The API allows companies to post job openings, and candidates to apply for jobs, and manage applications. It provides essential features such as user authentication, job posting management, and application tracking.

### Features
- **User Registration & Authentication**: Secure user registration and login using JWTs.
- **Job Listings**: Allows companies to create, edit, and delete job postings.
- **Job Application**: Candidates can apply to job listings.
- **Admin Panel**: Built-in Django admin panel for managing users, job postings, and applications.

---

## Getting Started

### Prerequisites
To run the project, ensure you have the following installed:
- Python 3.7+
- Django 3.2+
- PostgreSQL (or any other supported database)
- pipenv or virtualenv for dependency management

### Setup Instructions

#### 1. Clone the Repository

```
git clone https://github.com/JonathanM-A/job_portal_django.git
cd job_portal_django
```

#### 2. Create a Virtual Environment and Activate It
```
# Using built-in venv
source venv/bin/activate
```

#### 3. Install Dependencies

```
pip install -r requirements.txt
```

#### 4. Set up Environment Variables
Create a \`.env\` file in the root of the project and add the following keys:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/job_portal_db
ALLOWED_HOSTS=127.0.0.1,localhost
```

Ensure you have the correct credentials for your database setup.

#### 5. Database Setup

```
# Apply migrations
python manage.py migrate

# Create a superuser to access the admin panel
python manage.py createsuperuser
```

#### 6. Run the Development Server

```
python manage.py runserver
```

The API will be accessible at http://127.0.0.1:8000/

---

## API Endpoints

Here is a summary of the primary API endpoints:

### Auth
- **POST** `http://127.0.0.1:8000/register/`: Register a new user.
- **POST** `http://127.0.0.1:8000/login/`: Login and retrieve a JWT token.
- **POST** `http://127.0.0.1:8000/logout/`: Log out the user and invalidate the token.

### Jobs
- **GET** `http://127.0.0.1:8000/jobs/`: List all job postings.
- **POST** `http://127.0.0.1:8000/jobs/`: Create a new job posting (company only).
- **GET** `http://127.0.0.1:8000/jobs/<id>`: Retrieve details of a specific job posting.
- **PUT** `http://127.0.0.1:8000/jobs/<id>`: Update a job posting (company only).
- **DELETE** `http://127.0.0.1:8000/jobs/id`: Delete a job posting (company only).
- **POST** `http://127.0.0.1:8000/jobs/jobs/<id>/apply`: Apply for a job.

### Applications
- **GET** `http://127.0.0.1:8000/applications/`: View all applications (for candidates).
- **GET** `http://127.0.0.1:8000/applications/<id>`: Retrieve a specific application.
---

## Running Tests

To run the test suite:

```
python manage.py test
```

---

## Deployment

For production deployment, consider using a service like **Heroku**, **AWS**, or **DigitalOcean**. You will need to configure your production settings (\`DEBUG=False\`, proper database configuration, etc.).

Make sure to:

- Set \`ALLOWED_HOSTS\` for your domain.
- Set up **Gunicorn** or another WSGI server.
- Use **PostgreSQL** in production.
- Set up **CORS** if needed.

---

## Technologies Used

- **Django** - Python web framework for rapid development.
- **Django REST Framework** - For building a RESTful API.
- **PostgreSQL** - Relational database management system.
- **JWT** - JSON Web Token for authentication.

---

## Contributing

1. Fork the repository.
2. Create a new feature branch `git checkout -b feature-name`.
3. Commit your changes `git commit -m 'Add some feature'`.
4. Push to the branch `git push origin feature-name`.
5. Open a pull request.

---

## Contact

If you have any questions or issues, feel free to contact the repository owner:

- Email: kamajthomas@gmail.com
- GitHub: https://github.com/JonathanM-A
