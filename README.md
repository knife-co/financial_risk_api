# Financial Risk API

A Django REST API for financial risk assessment and management.

## Project Overview

- **users**: Represents a person using the application. This will handle authentication and authorization.
- **FinancialProfile**: A central table that links a User to all their financial data. This ensures all financial records are tied to a single user.
- **Income**: Represents a source of income for a user (e.g., salary, freelance).
- **Expense**: Represents a recurring monthly expense for a user (e.g., rent, gym membership).
- **Debt**: Represents a user's outstanding debt (e.g., credit card, student loan).
- **Asset**: Represents a user's financial assets (e.g., savings account, investment).
- **RiskAssessmentHistory**: Stores a snapshot of a user's risk score and the date it was calculated.


## Tech Stack

- **Backend**: Django 5.0.14
- **Database**: PostgreSQL (Production), PostgreSQL (Development)
- **Environment Management**: django-environ

## Project Structure

```
financial_risk_api/
├── manage.py
├── requirements.txt
├── .env.dev                    # Development environment variables
├── .env.prod                   # Production environment variables  
├── financial_risk_api/         # Main project directory
│   ├── settings/              # Split settings
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── __init__.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/                      # User management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py              # User model (if custom)
│   ├── serializers.py         # User serializers (registration, login, etc.)
│   ├── views.py               # Authentication views
│   ├── urls.py                # User-related URLs
│   ├── migrations/
│   │   └── __init__.py
│   └── tests.py
├── financialProfile/                  # Financial management app (consolidated)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py              # All financial models:
│   │                          #   - FinancialProfile
│   │                          #   - Income
│   │                          #   - Expense  
│   │                          #   - Debt
│   │                          #   - Asset
│   │                          #   - RiskAssessmentHistory
│   ├── serializers.py         # All financial serializers
│   ├── views.py               # All financial views/viewsets
│   ├── urls.py                # Financial API endpoints
│   ├── migrations/
│   │   └── __init__.py
│   └── tests.py
└── static/                     # Static files (optional)
    └── css/
    └── js/
    └── images/                 # User management
```

