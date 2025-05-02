# Real Estate Management System

A web-based application for managing real estate properties, owners, tenants, and leases.

## Features

- Property Management (add, edit, delete, view)
- Owner Management (add, edit, delete, view)
- Tenant Management (add, edit, delete, view)
- Lease Management (add, edit, terminate, view)
- Dashboard with key statistics and visualizations

## Tech Stack

- **Backend**: Python with Flask web framework
- **Database**: MySQL
- **Frontend**: HTML, Bootstrap 5, JavaScript

## Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd real-estate-management
```

2. Create a virtual environment and activate it:
```
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Configure environment variables:
Edit the `.env` file with your database credentials:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=real_estate_management
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

5. Initialize the database:
Run the MySQL script in your database client:
```
mysql -u root -p < create_database.sql
```

6. Run the application:
```
flask run
```

7. Access the application at http://localhost:5000

## Database Schema

The application uses the following database tables:
- Owners
- Properties
- Tenants
- Leases
- Payments

## License

[Include license information here] 
