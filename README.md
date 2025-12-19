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

## User Roles
HomeStay supports three types of users:

1. **Admin/Superuser**
   - Access to admin dashboard at `/admin-panel/`
   - Manage all users, listings, bookings, and payments
   - Approve or reject property listings
   - View platform statistics and revenue

2. **Host**
   - Create and manage property listings
   - Set availability and pricing
   - View incoming bookings
   - Users can become hosts by creating a listing

3. **Guest**
   - Browse and search properties
   - Make bookings and payments
   - Leave reviews
   - Default role for new signups

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

## Admin Dashboard Access

To access the admin dashboard:

1.  **Create a superuser** (if not done already):
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set username, email, and password.

2.  **Login and access**:
    - Regular Django admin: `http://127.0.0.1:8000/admin/`
    - Custom admin dashboard: `http://127.0.0.1:8000/admin-panel/`

3.  **Existing users** (if database is included):
    - Check if your `db.sqlite3` already has a superuser account
    - Try common credentials: `admin` / `admin123` (if pre-configured)

## Using the Platform

### As a Guest (Default)
1. **Sign up** on the homepage
2. **Browse listings** on the home page or use search/filters
3. **Select a property** and click on it to view details
4. **Book a stay**:
   - Choose check-in and check-out dates
   - Select number of guests
   - Proceed to payment (Stripe or JazzCash)
5. **Leave a review** after your stay

### Becoming a Host
1. **Log in** to your account (or sign up if you don't have one)
2. **Create a listing**:
   - Navigate to "Create Listing" (usually in user menu/profile)
   - Fill in property details (title, price, location, amenities, images)
   - Submit for admin approval
3. **Wait for approval**: Admins review listings before they go live
4. **Manage bookings**: View and manage incoming reservations once approved

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
