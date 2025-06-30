# Deal Radar - Day 1 Setup Instructions

## Quick Start Guide

### 1. Create Virtual Environment

```bash
# Windows
python -m venv deal_radar_env
deal_radar_env\Scripts\activate

# macOS/Linux
python3 -m venv deal_radar_env
source deal_radar_env/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

```bash
# Copy example environment file
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Edit .env file with your settings:
# - Set SECRET_KEY
# - Configure database settings
# - Add other API keys as needed
```

### 4. Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Development Commands

### Create new migrations

```bash
python manage.py makemigrations
```

### Run tests

```bash
python manage.py test
```

### Access Django shell

```bash
python manage.py shell
```

### Collect static files (for production)

```bash
python manage.py collectstatic
```

## Project Structure

deal_radar/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── deal_radar/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py
├── users/
│   ├── models.py (UserProfile)
│   ├── views.py (Auth views)
│   ├── urls.py
│   └── apps.py
├── products/
│   ├── models.py (Product, PriceHistory, TrackedProduct, DealAlert)
│   └── apps.py
├── notifications/
│   └── apps.py
├── subscriptions/
│   └── apps.py
├── templates/
│   ├── base.html
│   └── users/
│       └── home.html
└── .github/
    └── workflows/
        └── ci.yml

## Day 1 Goals Status

- [x] Django project setup
- [x] Apps created (users, products, notifications, subscriptions)
- [x] Database models defined
- [x] Basic templates created
- [x] Requirements.txt configured
- [x] Environment setup
- [x] GitHub CI/CD pipeline
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Database migrations run
- [ ] Development server running

## Ready for Day 2

Once the setup above is completed, we'll be ready to move to Day 2:

- User authentication forms
- Product CRUD operations
- Dashboard improvements
- Admin interface setup
