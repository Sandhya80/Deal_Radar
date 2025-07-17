# Deal Radar

**Never Miss a Deal Again!**  
Deal Radar is a robust Django-based web application that empowers users to track product prices across major e-commerce platforms and receive real-time alerts when deals are available. With a modern, responsive interface and automated background processing, Deal Radar ensures you never miss a price drop on your favorite products.

---

## 🔄 App Workflow Overview

1. **Add Products to Track:**  
   Add products by pasting a URL from a supported e-commerce site or by selecting from existing products in the database.

2. **Set Target Price:**  
   Specify a target price for each product. You’ll be notified when the product reaches or drops below this price.

3. **Automated Price Tracking:**  
   The system regularly scrapes product pages using background Celery tasks to check for price changes.

4. **Receive Alerts:**  
   When a product’s price drops to or below your target, Deal Radar sends real-time alerts via email, WhatsApp, or SMS (based on your preferences).

5. **Dashboard & Management:**  
   View all tracked products, manage alerts, and see your savings and triggered alerts on a personalized dashboard.

6. **Subscription & Billing:**  
   Unlock premium features (like more frequent checks or additional notification channels) via Stripe-powered subscriptions.

---

## 🚦 Project Status

- **Phase 1: Foundation & Authentication** ✅ Complete  
- **Phase 2: MVP Functionality** ✅ Complete  
- **Phase 3: Automation & Alerts** ✅ Complete  
- **Phase 4: Polish & Monetization** ✅ Complete  

---

## ✅ Completed Features by Phase

### Phase 1: Foundation & Authentication

- Modular Django apps: `users`, `products`, `notifications`, `subscriptions`
- Comprehensive code documentation and comments
- Dependency management (`requirements.txt`, `.env.example`, `.gitignore`)
- Database models for users, products, price history, and alerts
- User authentication (registration, login, logout) with Django AllAuth
- Profile management with notification preferences and subscription tiers
- Responsive Bootstrap 5 UI with base, dashboard, and CRUD templates

### Phase 2: MVP Functionality

- Automated web scraping for supported e-commerce sites (Amazon, eBay, Argos, etc.)
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

## 🐞 Debugging Methods Used

- **Django Debug Toolbar**: For inspecting SQL queries, cache usage, and template context.
- **Python Logging**: Configured in `settings.py` for error, warning, and info logs.
- **Custom Error Pages**: User-friendly error templates for 404/500.
- **Unit Tests**: Django’s test framework for core logic and integration.
- **Manual Testing**: Django shell (`python manage.py shell`) and admin panel for data validation.
- **Celery Task Monitoring**: Celery logs and Flower (optional) for background task debugging.
- **AI Assistance**: GitHub Copilot for code review, suggestions, and troubleshooting.

---

## 🗄️ Database Schema

Below is a simplified schema of the main tables and relationships in Deal Radar:

```mermaid
erDiagram
    USER ||--o{ PRODUCT_TRACKING : tracks
    USER ||--o{ PRICE_ALERT : creates
    USER ||--|| USER_PROFILE : has
    USER_PROFILE }|..|{ SUBSCRIPTION_PLAN : subscribes
    PRODUCT ||--o{ PRODUCT_TRACKING : is_tracked
    PRODUCT ||--o{ PRICE_HISTORY : has
    PRODUCT_TRACKING ||--o{ PRICE_ALERT : has
    PRODUCT ||--o{ PRICE_ALERT : alerts_for
    PRODUCT }|..|{ CATEGORY : belongs_to

    USER {
        int id PK
        string username
        string email
        string password
    }
    USER_PROFILE {
        int id PK
        int user_id FK
        bool email_notifications
        bool whatsapp_notifications
        string notification_frequency
        string whatsapp_number
        int subscription_plan_id FK
    }
    SUBSCRIPTION_PLAN {
        int id PK
        string name
        decimal price
        string stripe_plan_id
    }
    PRODUCT {
        int id PK
        string name
        string url
        string site_name
        string image_url
        int category_id FK
        datetime created_at
        datetime updated_at
    }
    CATEGORY {
        int id PK
        string name
        string emoji
    }
    PRODUCT_TRACKING {
        int id PK
        int user_id FK
        int product_id FK
        decimal target_price
        string notes
        datetime created_at
    }
    PRICE_HISTORY {
        int id PK
        int product_id FK
        decimal price
        datetime checked_at
    }
    PRICE_ALERT {
        int id PK
        int user_id FK
        int product_id FK
        int tracking_id FK
        decimal target_price
        bool is_triggered
        bool is_enabled
        datetime created_at
        datetime triggered_at
    }
```

### 📑 Database Schema Explained

- **USER**: Stores user account information (username, email, password).
- **USER_PROFILE**: Extends user info with notification preferences, WhatsApp number, and subscription plan.
- **SUBSCRIPTION_PLAN**: Lists available subscription plans (name, price, Stripe plan ID).
- **PRODUCT**: Contains product details (name, URL, site, image, category, timestamps).
- **CATEGORY**: Defines product categories (name, emoji).
- **PRODUCT_TRACKING**: Links users to products they are tracking, with target price and notes.
- **PRICE_HISTORY**: Records historical prices for each product over time.
- **PRICE_ALERT**: Stores alerts for users when a product hits their target price, including status

---

## 🗂️ Files Involved & Workflow

**How the database schema maps to your project files and workflow:**

- **Models (Database Tables)**
  - `products/models.py`: `Product`, `Category`, `ProductTracking`, `PriceHistory`, `PriceAlert`
  - `users/models.py`: `UserProfile`
  - `subscriptions/models.py`: `SubscriptionPlan`
  - Django’s built-in `User` model: from `django.contrib.auth.models`

- **Views (Business Logic & Workflow)**
  - `products/views.py`: Add/track products, dashboard, product detail, price history, alerts
  - `users/views.py`: Profile management, authentication, notification preferences
  - `subscriptions/views.py`: Subscription and billing management

- **Forms (User Input)**
  - `products/forms.py`: Product add/edit, tracking, alert forms
  - `users/forms.py`: Profile update, notification settings
  - `subscriptions/forms.py`: Subscription plan selection

- **Templates (Frontend/UI)**
  - `templates/products/`: `add_product.html`, `dashboard.html`, `product_detail.html`, `home.html`, etc.
  - `templates/users/`: `profile.html`, `login.html`, `signup.html`
  - `templates/subscriptions/`: `billing.html`, `upgrade.html`
  - `templates/base.html`: Main layout and navigation

- **Celery Tasks (Background Processing)**
  - `products/tasks.py`: Price scraping, alert sending

**Typical Workflow:**

1. **User Registration/Login**  
   - `users/views.py`, `users/forms.py`, `templates/registration/signup.html`, `login.html`
   - Uses Django’s `User` model and `UserProfile`

2. **Add Product to Track**  
   - `products/views.py` (`add_product` view), `products/forms.py` (`AddProductForm`), `templates/products/add_product.html`
   - Models: `Product`, `ProductTracking`, `Category`

3. **Set Target Price & Preferences**  
   - `products/forms.py`, `users/forms.py`
   - Models: `ProductTracking`, `UserProfile`

4. **Automated Price Tracking**  
   - `products/tasks.py` (Celery)
   - Updates `PriceHistory`, checks for `PriceAlert` triggers

5. **Receive Alerts**  
   - `products/tasks.py` (Celery)
   - Sends notifications via Twilio/SMIP
   - Updates `PriceAlert`

6. **Dashboard & Management**  
   - `products/views.py` (`dashboard` view), `templates/products/dashboard.html`
   - Shows tracked products, price history, alerts

7. **Subscription & Billing**  
   - `subscriptions/views.py`, `subscriptions/forms.py`
   - Models: `SubscriptionPlan`, `UserProfile`
   - `templates/subscriptions/billing.html`

**Example File Paths:**

- `d:\Sandhya_H\Deal_Radar\products\models.py`
- `d:\Sandhya_H\Deal_Radar\users\models.py`
- `d:\Sandhya_H\Deal_Radar\subscriptions\models.py`
- `d:\Sandhya_H\Deal_Radar\products\views.py`
- `d:\Sandhya_H\Deal_Radar\templates\products\add_product.html`
- `d:\Sandhya_H\Deal_Radar\products\tasks.py`
