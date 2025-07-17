# Deal Radar

**Never Miss a Deal Again!**  
A Django-based web application that tracks product prices across e-commerce platforms and sends real-time alerts when deals are available.

---

## 🚦 Project Status

**Phase 1: Foundation & Authentication** ✅ *Complete*  
**Phase 2: MVP Functionality** ✅ *Complete*  
**Phase 3: Automation & Alerts** ✅ *Complete*  
**Phase 4: Polish & Monetization** ✅ *Complete*  

---

## ✅ Completed Features by Phase

### Phase 1: Foundation & Authentication

- Django project structure with modular apps: `users`, `products`, `notifications`, `subscriptions`
- Comprehensive code documentation and comments
- Dependency management (`requirements.txt`, `.env.example`, `.gitignore`)
- Database models for users, products, price history, and alerts
- User authentication (registration, login, logout) with Django AllAuth
- Profile management with notification preferences and subscription tiers
- Bootstrap 5 responsive UI with base, dashboard, and CRUD templates

### Phase 2: MVP Functionality

- Automated web scraping engine for supported e-commerce sites (Amazon, eBay, Argos, etc.)
- Celery background task system for scheduled scraping and notifications
- Redis integration for task queue management
- Enhanced dashboard with real-time scraping status and product updates
- Admin tools for manual scraping and product management
- Product search, category browsing, and filtering

### Phase 3: Automation & Alerts

- Email notifications for price drops and triggered alerts
- SMS/WhatsApp integration via Twilio for instant alerts
- Celery task scheduling for periodic scraping and alert delivery
- User-configurable alert preferences (frequency, channels)
- Daily/weekly summary emails for tracked products and triggered alerts

### Phase 4: Polish & Monetization

- Stripe subscription system for premium features
- Billing management and upgrade/downgrade flows
- Unit and integration testing for core features
- Security hardening (environment variables, HTTPS, input validation)
- Final deployment to Heroku (or similar cloud platform)
- Cloudinary integration for product image storage
- UI/UX polish and accessibility improvements

---

## 🚀 Getting Started

### 1. Install Dependencies & Setup Environment

```bash
# Create virtual environment
python -m venv deal_radar_env
deal_radar_env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env
# Edit .env with your database and API credentials
```

### 2. Database Setup

```bash
# Create and run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 3. Run Development Server

```bash
python manage.py runserver
```

### 4. Start Celery Worker (for background tasks)

```bash
celery -A deal_radar worker -l info
celery -A deal_radar beat -l info
```

### 5. (Optional) Start Redis Server

- Ensure Redis is running for Celery task queue.

---

## 🏗️ Architecture Overview

```
Frontend (Bootstrap + Django Templates)
    ↕
Django Views + Django REST Framework
    ↕
PostgreSQL (Users, Products, Price History)
    ↕
Celery Workers (Price Scraping, Alerts)
    ↕
Redis (Task Queue)
    ↕
Notifications (Email/SMS/WhatsApp)
    ↕
Stripe (Billing)
    ↕
Cloudinary (Image Storage)
```

---

## ✨ Features Overview

### Phase 1: Foundation
- [x] User authentication system (register, login, logout)
- [x] Product tracking models and price history
- [x] Basic dashboard UI and CRUD for products
- [x] Responsive Bootstrap UI

### Phase 2: MVP Functionality
- [x] Web scraping for supported sites
- [x] Price drop detection and history
- [x] Dashboard with real data and search/filter
- [x] Admin tools for scraping and product management

### Phase 3: Automation & Alerts
- [x] Email and WhatsApp/SMS notifications
- [x] Celery task scheduling for scraping and alerts
- [x] User alert preferences (frequency, channels)
- [x] Daily/weekly summary emails

### Phase 4: Polish & Monetization
- [x] Stripe subscription system (Free/Basic/Premium)
- [x] Billing management and upgrade/downgrade
- [x] Unit and integration testing
- [x] Security hardening and accessibility
- [x] Final deployment and documentation

---

## 🛠️ Tech Stack

- **Backend**: Django 5.0, Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Task Queue**: Celery + Redis
- **Scraping**: BeautifulSoup, Selenium
- **Notifications**: Twilio (SMS/WhatsApp), SMTP (Email)
- **Payments**: Stripe
- **Deployment**: Heroku (or similar)
- **Storage**: Cloudinary (Images)

---

## 📋 Assessment Criteria Alignment

- **Authentication & Role-Based Access**: Django Auth + User Profiles
- **Database Design & CRUD**: PostgreSQL + Django ORM
- **Front-End Design & UX**: Bootstrap + Responsive Design
- **Version Control**: Git + GitHub
- **Deployment**: Heroku Ready
- **Custom Data Modeling**: Product/Price/User Models
- **Security**: Environment Variables + HTTPS

---

## 🤝 Support

For questions or issues, please create an issue in this repository.

---

**Built with Django, Celery, Stripe, and AI assistance for debugging**
