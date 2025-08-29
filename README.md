
# Financial Risk API

A Django REST API that empowers users to track, analyze, and manage their personal finances. The system aggregates income, expenses, debts, and assets, then calculates a comprehensive financial risk score using multiple factors. Users receive actionable insights, historical risk tracking, and secure authentication, making it ideal for personal finance management, advisory platforms, or financial wellness applications.

## Features

- User authentication (JWT)
- Financial profile management (income, expenses, debts, assets)
- Automated risk assessment with detailed scoring
- Historical risk tracking
- Bulk financial data creation
- Staff/admin support for viewing all profiles

## API Overview

### Authentication
- Uses JWT for secure API access
- Endpoints: `/api/users/token/verify`, `/api/users/token/refresh/`, `/api-auth/` (DRF browsable login)


### Key Endpoints
- `/api/users/register/` - Register a new user
- `/api/users/login/` - Login and obtain JWT token
- `/api/users/profile/` - Get user profile
- `/api/users/token/refresh/` - Refresh JWT token
- `/api/users/token/verify/` - Verify JWT token

- `/api/financial/profiles/` - List/create financial profiles
- `/api/financial/profile/` - Get/update/delete current user's financial profile

- `/api/financial/incomes/` - List/create incomes
- `/api/financial/incomes/<id>/` - Retrieve/update/delete an income

- `/api/financial/expenses/` - List/create expenses
- `/api/financial/expenses/<id>/` - Retrieve/update/delete an expense

- `/api/financial/debts/` - List/create debts
- `/api/financial/debts/<id>/` - Retrieve/update/delete a debt

- `/api/financial/assets/` - List/create assets
- `/api/financial/assets/<id>/` - Retrieve/update/delete an asset

- `/api/financial/risk-assessments/` - List/create risk assessments
- `/api/financial/risk-assessments/<id>/` - Retrieve/delete a risk assessment

- `/api/financial/summary/` - Get full financial summary and risk factors
- `/api/financial/bulk-create/` - Bulk create financial data
- `/api/financial/calculate-risk-assessment/` - Calculate and create a new risk assessment

#### Example: Financial Summary Response
```json
{
    "profile_id": 3,
    "user": "Nifemzy",
    "last_assessed": "2025-08-28T15:06:40.288790Z",
    "financial_metrics": {
        "total_monthly_income": 20000.0,
        "total_monthly_expenses": 3566.6666666666665,
        "total_debt_balance": 4000.0,
        "total_assets_value": 2000.0,
        "net_worth": -2000.0,
        "debt_to_income_ratio": 1.25
    },
    "risk_factors": {
        "debt_to_income_ratio": 10,
        "emergency_fund_ratio": 85,
        "high_interest_debt": 5,
        "income_stability": 70,
        "expense_coverage": 5,
        "debt_diversity": 20
    },
    "counts": {
        "income_sources": 1,
        "expense_categories": 4,
        "debts": 2,
        "assets": 1,
        "risk_assessments": 1
    },
    "latest_risk_assessment": {
        "score": 32,
        "level": "Low Risk",
        "color": "#84cc16"
    },
    "profile_completeness": {
        "is_complete": true,
        "has_income": true,
        "has_expenses": true,
        "has_debts": true,
        "has_assets": true
    }
}
```

## Risk Assessment Logic


Risk score is calculated using the following factors:

- **Debt-to-income ratio (25%)**: Measures the percentage of your income that goes toward debt payments. Lower ratios indicate better financial health and lower risk.
- **Emergency fund coverage (20%)**: Assesses how many months of expenses your liquid assets can cover. More coverage means greater financial security and lower risk.
- **High-interest debt (20%)**: Evaluates the proportion of your debt that has a high interest rate (e.g., >15%). High levels of high-interest debt increase financial risk.
- **Income stability (15%)**: Looks at the diversity and number of your income sources. Multiple sources mean more stability and lower risk.
- **Expense coverage (15%)**: Compares your total expenses to your total income. Spending less than you earn is low risk; spending more is high risk.
- **Debt diversity (5%)**: Considers the variety of debt types you have. Having many different types of debt can increase risk.

Each factor is scored (0 = lowest risk, 100 = highest risk) and weighted as shown above to produce the final risk score (0-100).

## Getting Started

1. Clone the repo: `git clone ...`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up `.env.dev` and `.env.prod` files
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

## Project Overview


- **users app**: Handles authentication, authorization, and user profile management.
- **FinancialProfile app**: Centralizes all financial data for each user. Contains the following models:
    - **FinancialProfile**: Links a User to their financial records.
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
|   └── risk_calculator.py     # Aggregates the risk factors considered for risk assessment
└── static/                     # Static files (optional)
    └── css/
    └── js/
    └── images/                 # User management
```

