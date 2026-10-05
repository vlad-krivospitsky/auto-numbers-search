# Auto Numbers Search

A Django web application for searching Ukrainian vehicle license plates with real-time HTMX-powered search, staff-controlled CRUD management, and role-based access control.

## Features

- **Real-time search** — instant license plate lookup with HTMX (no page reload)
- **Bilingual input** — automatically handles mixed Cyrillic/Latin character input (e.g. `AA` ↔ `АА`)
- **Vehicle registry** — detailed records: brand, model, year, fuel type, body type, region, registration date
- **Role-based access** — regular users can search and view; staff can create, edit, and delete records
- **Admin panel** — manage users and toggle staff roles from a built-in user management page
- **Responsive UI** — Bootstrap 5 with pagination, sidebar navigation, and loading indicators


## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/auto-numbers-search.git
cd auto-numbers-search
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and set the required values:

```ini
# Generate a new secret key:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY=your-secret-key-here

DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# API key for vehicle images (carimagesapi.com)
CAR_IMAGES_API_KEY=your-carimagesapi-key-here
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Seed the database

Populate Ukrainian regions (required before importing vehicles):

```bash
python manage.py seed_regions
```

Optionally, import vehicles from `db.json` (place the file in the project root):

```bash
python manage.py load_json_data
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 📁 Project Structure

```
auto-numbers-search/
├── apps/
│   ├── accounts/
│   └── vehicles/
│       ├── models/
│       │   ├── vehicle.py
│       │   └── region.py
│       ├── management/commands/
│       │   ├── seed_regions.py    # Seed Ukrainian regions
│       │   └── load_json_data.py  # Import vehicles from JSON
│       ├── views.py
│       ├── forms.py
│       └── urls.py
├── config/
│   ├── settings.py
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── accounts/
│   └── vehicles/
│       └── partials/   
├── static/
├── .env.example         
├── .gitignore
├── manage.py
└── requirements.txt
```

## 🧪 Running Tests

```bash
python manage.py test apps.vehicles apps.accounts --verbosity=2
```
