# UZNR backend

Django + Django REST Framework backend for the UZNR site. Django's built-in
admin (`/admin/`) is the CMS — staff log in there to add/edit news posts and
members, including uploading thumbnail/logo images directly. The public API
(read-only) is what the Vue frontend consumes.

`content/seed_data/*.json` holds the news/members content originally scraped
from uznr.me. `python manage.py import_seed` loads it into the database and
downloads the real images into `media/` — safe to re-run, it skips images
that already exist.

## Setup

Windows:
```
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe manage.py migrate
venv\Scripts\python.exe manage.py import_seed
venv\Scripts\python.exe manage.py createsuperuser
```

Linux/WSL:
```
python3 -m venv venv_linux
source venv_linux/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py import_seed
python manage.py createsuperuser
```

## Run

Windows: `venv\Scripts\python.exe manage.py runserver 8000`
Linux/WSL: `python manage.py runserver 8000`

- Public API: http://localhost:8000/api/
- Admin/CMS: http://localhost:8000/admin/

## Endpoints

- `GET /api/health`
- `GET /api/news` — list news, newest first
- `GET /api/news/{slug}` — single news item
- `GET /api/members` — list association members

Writes (create/edit/delete news, members, upload images) happen through
`/admin/`, not the API — the public API is read-only by design.
