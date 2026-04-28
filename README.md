# ReWear

ReWear is now a Django application with server-rendered templates and a MySQL database.

## Stack

- Backend: Django
- Frontend: Django templates
- Database: MySQL
- File uploads: Django media storage

## Working flows

- Sign up with email and password
- Log in and log out using Django auth
- Upload a new clothing item with an image
- Browse listed items
- View your own dashboard and item listings

## Run locally

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Copy the environment file and fill in your MySQL credentials:

```bash
copy .env.example .env
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Start the server:

```bash
python manage.py runserver
```

5. Open:

- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Notes

- Uploaded files are stored in the local `media/` folder.
- Django reads MySQL connection values from the root `.env` file.
