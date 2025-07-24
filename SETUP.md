# Deal Radar – Setup Guide

This guide will help you set up Deal Radar on your local machine and deploy it to Heroku.

---

## Prerequisites

- Python 3.8+
- pip
- Git
- (Optional for local production) PostgreSQL
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- A free [Heroku](https://heroku.com/) account

---

## Local Installation Steps

1. **Clone the repository**

   ```sh
   git clone https://github.com/yourusername/deal-radar.git
   cd deal-radar
   ```

2. **Create and activate a virtual environment**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Fill in your Stripe, Cloudinary, and other keys

5. **Apply migrations**

   ```sh
   python manage.py migrate
   ```

6. **Create a superuser (admin)**

   ```sh
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```sh
   python manage.py runserver
   ```

8. **Access the app**
   - Open [http://localhost:8000](http://localhost:8000) in your browser

---

## Deploying to Heroku

1. **Login to Heroku**

   ```sh
   heroku login
   ```

2. **Create a new Heroku app**

   ```sh
   heroku create your-app-name
   ```

3. **Set up Heroku Postgres (recommended for production)**

   ```sh
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set environment variables on Heroku**
   - You can set each variable using:

     ```sh
     heroku config:set KEY=your_value
     ```

   - Set all required variables (SECRET_KEY, DEBUG, STRIPE keys, CLOUDINARY_URL, etc.)

5. **Push your code to Heroku**

   ```sh
   git push heroku main
   ```

   *(or `git push heroku master` if your default branch is master)*

6. **Run migrations on Heroku**

   ```sh
   heroku run python manage.py migrate
   ```

7. **Create a superuser on Heroku**

   ```sh
   heroku run python manage.py createsuperuser
   ```

8. **Collect static files**

   ```sh
   heroku run python manage.py collectstatic --noinput
   ```

9. **Open your deployed app**

   ```sh
   heroku open
   ```

---

## Troubleshooting

- If you encounter issues, check your environment variables and dependencies.
- For Stripe or Cloudinary errors, verify your API keys and dashboard settings.
- For Heroku deployment issues, check logs with:

  ```sh
  heroku logs --tail
  ```

---

For further help, open an issue or contact the maintainer.
