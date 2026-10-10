# Campus Marketplace

Campus Marketplace is a web application for students to buy and sell second-hand items within their campus community. It is built with Django and PostgreSQL and provides a simple way to create listings, discover available products, and communicate with other users.

## Live Website

[Visit Campus Marketplace](https://campus-marketplace-tn65.onrender.com)

> The free hosting service may take a short time to respond after a period of inactivity.

## Features

- User registration, login, and logout
- User dashboard and profile
- Create, view, edit, and delete product listings
- Product descriptions, prices in euros (€), and image uploads
- Mark listings as available or sold
- Search and filter listings
- View individual listing details
- Messaging between users and an inbox
- Responsive interface for desktop and mobile screens

## Technologies Used

- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Static files:** WhiteNoise
- **Deployment:** Render
- **Version control:** Git and GitHub

## Running the Project Locally

### Prerequisites

- Python installed
- PostgreSQL installed and running
- Git (optional, for cloning the repository)

### 1. Clone the repository

```bash
git clone https://github.com/Tefo23/campus-marketplace.git
cd campus-marketplace
```

If the repository is private, you will need permission to access it.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root. Set the values to match your own local PostgreSQL database:

```dotenv
DJANGO_SECRET_KEY=replace-with-your-own-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=your_local_database_name
DB_USER=your_local_database_user
DB_PASSWORD=your_local_database_password
DB_HOST=localhost
DB_PORT=5432
```

**Security:** Do not commit `.env`, database passwords, or secret keys to GitHub. Use separate credentials for local development and deployment.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Testing

Run Django's automated tests with:

```bash
python manage.py test
```

You can also manually test registration, login, listing creation, editing, searching, messaging, and responsive layouts.

## Deployment

The application is deployed as a Django web service on Render, with a separate Render PostgreSQL database.

The deployment uses environment variables for sensitive configuration, Gunicorn to run the application, and WhiteNoise to serve static assets.

## Known Limitation

**Uploaded listing images may not display on the deployed website.** Render's free web service does not provide persistent local file storage, and production media delivery is not yet configured. The image upload feature can work in local development, but hosted uploads require an external media storage service such as Cloudinary for reliable display and persistence.

## Future Improvements

- Integrate cloud storage for listing images
- Improve listing search and filtering
- Expand user messaging and notifications
- Continue refining the mobile experience

## Project Context

This project was developed as coursework to demonstrate full-stack web development with Django, PostgreSQL, authentication, CRUD operations, and deployment.
