# FinancialProfile/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Option 1: Using regular URL patterns (recommended for this structure)
urlpatterns = [
    # Financial Profile endpoints
    path('profile/', views.FinancialProfileDetailView.as_view(), name='financial-profile-detail'),
    path('profiles/', views.FinancialProfileListCreateView.as_view(), name='financial-profile-list'),
    
    # Income endpoints
    path('incomes/', views.IncomeListCreateView.as_view(), name='income-list'),
    path('incomes/<int:pk>/', views.IncomeDetailView.as_view(), name='income-detail'),
    
    # Expense endpoints
    path('expenses/', views.ExpenseListCreateView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense-detail'),
    
    # Debt endpoints
    path('debts/', views.DebtListCreateView.as_view(), name='debt-list'),
    path('debts/<int:pk>/', views.DebtDetailView.as_view(), name='debt-detail'),
    
    # Asset endpoints
    path('assets/', views.AssetListCreateView.as_view(), name='asset-list'),
    path('assets/<int:pk>/', views.AssetDetailView.as_view(), name='asset-detail'),
    
    # Risk Assessment endpoints
    path('risk-assessments/', views.RiskAssessmentListCreateView.as_view(), name='risk-assessment-list'),
    path('risk-assessments/<int:pk>/', views.RiskAssessmentDetailView.as_view(), name='risk-assessment-detail'),
    
    # Custom endpoints
    path('summary/', views.financial_summary, name='financial-summary'),
    path('bulk-create/', views.bulk_create_financial_data, name='bulk-create-financial-data'),

    # Risk calculator endpoints
    path('calculate-risk-assessment/', views.calculate_risk_assessment, name='calculate-risk-assessment'),
]
