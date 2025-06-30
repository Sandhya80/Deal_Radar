# Deal Radar

**Never Miss a Deal Again!** - A Django-based web application that tracks product prices across e-commerce platforms and sends real-time alerts when deals are available.

## Project Status

**Phase 1: Foundation & Authentication** *Complete*

### Phase 1 Completed Features

1. **Django Project Structure**
   - Main project: `deal_radar`
   - Apps: `users`, `products`, `notifications`, `subscriptions`
   - Comprehensive code documentation and comments

2. **Dependencies Configuration**
   - `requirements.txt` with all necessary packages
   - Environment configuration with detailed `.env.example`
   - Proper `.gitignore` setup

3. **Database Models & Migrations**
   - User authentication and profiles with subscription tiers
   - Product tracking system with price history
   - Deal alerts system with notification preferences
   - All migrations created and applied

4. **Authentication System**
   - Django AllAuth integration for advanced authentication
   - User registration, login, logout functionality
   - Profile management with notification preferences
   - Subscription tier management (Free/Premium)

5. **Basic UI Framework**
   - Bootstrap 5 integration with responsive design
   - Base template with navigation and styling
   - Dashboard template for product management
   - Product add/edit/delete templates

6. **Code Documentation**
   - Comprehensive comments in all major files
   - Business logic explanations
   - Phase implementation strategy documented
   - API endpoint documentation

### Ready for Phase 2

All foundation components are in place and fully documented. The application now has:

- Working authentication system
- Complete database schema
- Basic CRUD operations for products
- Responsive UI framework
- Comprehensive code documentation

**Current State**: Fully functional Phase 1 application ready for web scraping implementation in Phase 2.

1. **Database Models**
   - User authentication and profiles
   - Product tracking system
   - Price history tracking
   - Deal alerts system

2. **Basic UI Framework**
   - Bootstrap 5 integration
   - Responsive base template
   - Home page template

### Next Steps (Day 1 Completion)

1. **Install Dependencies & Setup Environment**

   ```bash
   # Create virtual environment
   python -m venv deal_radar_env
   deal_radar_env\Scripts\activate  # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Setup environment
   copy .env.example .env
   # Edit .env with your database credentials
   ```

2. **Database Setup**

   ```bash
   # Create and run migrations
   python manage.py makemigrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   ```

3. **Run Development Server**

   ```bash
   python manage.py runserver
   ```

## Architecture Overview

Frontend (Bootstrap + Django Templates)
    ↕
Django Views + Django REST Framework
    ↕
PostgreSQL (Users, Products, Price History)
    ↕
Celery Workers (Price Scraping Tasks)
    ↕
Notifications (Email/SMS/WhatsApp)
```

## Features Overview

### Phase 1 (Days 1-3): Foundation
- [x] User authentication system
- [x] Product tracking models
- [x] Basic dashboard UI
- [x] CRUD operations for products

### Phase 2 (Days 4-7): MVP Functionality
- [ ] Web scraping implementation
- [ ] Price drop detection
- [ ] Dashboard with real data
- [ ] Heroku deployment

### Phase 3 (Days 8-10): Automation & Alerts
- [ ] Email notifications
- [ ] SMS/WhatsApp integration
- [ ] Celery task scheduling
- [ ] Alert preferences

### Phase 4 (Days 11-14): Polish & Monetization
- [ ] Stripe subscription system
- [ ] Unit testing
- [ ] Security hardening
- [ ] Final deployment

## 🛠️ Tech Stack

- **Backend**: Django 5.0, Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Task Queue**: Celery + Redis
- **Scraping**: BeautifulSoup, Selenium
- **Notifications**: Twilio (SMS/WhatsApp), SMTP (Email)
- **Payments**: Stripe
- **Deployment**: Heroku
- **Storage**: Cloudinary (Images)

## Assessment Criteria Alignment

- **Authentication & Role-Based Access**: Django Auth + User Profiles
- **Database Design & CRUD**: PostgreSQL + Django ORM
- **Front-End Design & UX**: Bootstrap + Responsive Design
- **Version Control**: Git + GitHub
- **Deployment**: Heroku Ready
- **Custom Data Modeling**: Product/Price/User Models
- **Security**: Environment Variables + HTTPS

## Support

For questions about this project, please create an issue in this repository.

---
**Built with using Django & AI assistance for debugging**
