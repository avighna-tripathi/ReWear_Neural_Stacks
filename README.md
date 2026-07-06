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

## Cloudinary on Render free tier

Render free web services do not support persistent disks. To make uploaded product images survive redeploys, use Cloudinary for media storage.

1. Create a free Cloudinary account at [Cloudinary](https://cloudinary.com/).
2. In the Cloudinary console, open your API Keys page and copy the `CLOUDINARY_URL` value or build it in this format:

```env
CLOUDINARY_URL=cloudinary://<your_api_key>:<your_api_secret>@<your_cloud_name>
```

3. In Render, open your web service and go to `Environment`.
4. Add the `CLOUDINARY_URL` environment variable.
5. Redeploy the service.

This project is already configured to:
- use Cloudinary automatically for all `ImageField` uploads whenever `CLOUDINARY_URL` is present
- keep WhiteNoise for static files
- fall back to local `media/` storage when `CLOUDINARY_URL` is not set

### Restore the bundled sample product images into Cloudinary

If your deployed database already has the seeded sample products but their image files are missing, open the Render shell and run:

```bash
python manage.py migrate
python manage.py seed_sample_data
python manage.py restore_sample_images
```

If users and items already exist, you can usually skip directly to:

```bash
python manage.py restore_sample_images
```

Use this to overwrite existing stored image paths if needed:

```bash
python manage.py restore_sample_images --force
```

After that, open the deployed site and verify that product images are visible on browse and item detail pages.

## Render persistent disk for uploads

If you upgrade to a paid Render instance later, you can use a persistent disk instead of Cloudinary.

If you deploy on Render, product images should be stored on a persistent disk instead of the app container filesystem.

1. In Render, attach a persistent disk to your web service.
2. Mount the disk at `/var/data`.
3. Add the environment variable `MEDIA_ROOT=/var/data/media`.
4. Keep `MEDIA_URL=/media/` or leave it unset to use the default.
5. Redeploy the service.

After this, newly uploaded product images will be written to the persistent disk and will survive redeploys and restarts.

Important:
- Static files are handled separately by WhiteNoise.
- Existing images that were uploaded before the disk was attached may need to be re-uploaded once so they are copied onto the persistent disk.

### Restore the bundled sample product images

If your deployed database already has the seeded sample products but their image files are missing, run:

```bash
python manage.py restore_sample_images
```

This command copies the bundled sample images from the repository into your active Django media storage, which means they will be written onto the Render persistent disk when `MEDIA_ROOT` points there.
