# HomeStay - Vacation Rental Platform

## Project Overview
HomeStay is a comprehensive vacation rental platform built with Django. It allows users to browse listings, book stays, and manage their profile. Hosts can list properties, manage availability, and view bookings.

## Features
- **User Authentication**: Secure login, signup, and email verification.
- **Property Listings**: Detailed property pages with images, amenities, and location.
- **Search & Filter**: Find properties by location, date, and other criteria.
- **Booking System**: Secure booking flow with date validation and pricing calculation.
- **Host Dashboard**: Manage listings and view incoming bookings.
- **Reviews & Ratings**: Leave feedback on stays.

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation & Setup

1.  **Clone or Extract the Project**
    Open your terminal/command prompt and navigate to the project folder.

2.  **Create a Virtual Environment**
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv .venv
    ```
    Activate the virtual environment:
    - **Windows**: `.venv\Scripts\activate`
    - **Mac/Linux**: `source .venv/bin/activate`

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Configuration (Optional)**
    The project is configured to run out-of-the-box for development.
    *   **Default Mode**: Uses a development `SECRET_KEY`, `DEBUG=True`, and Console Email Backend.
    *   **Production**: For production, create a `.env` file based on `.env.example`.

5.  **Database Migration**
    Apply the database migrations to set up the schema.
    ```bash
    python manage.py migrate
    ```
    *(Note: If `db.sqlite3` is included, this might already be done, but running it again is safe)*

6.  **Create a Superuser (Admin) (Optional)**
    To access the Django admin panel:
    ```bash
    python manage.py createsuperuser
    ```

## Running the Application

1.  Start the development server:
    ```bash
    python manage.py runserver
    ```

2.  Open your browser and navigate to:
    `http://127.0.0.1:8000/`

## Project Structure
- `config/`: Main project configuration (settings, urls).
- `core/`: Core functionality and base templates.
- `listings/`: Main application logic (models, views for listings and bookings).
- `custom_admin/`: Custom dashboard for admin/host management.
- `static/`: CSS, JavaScript, and static images.
- `media/`: User-uploaded content (property images, avatars).
- `scripts/`: Utility and verification scripts.

## License
[Your License Here]
