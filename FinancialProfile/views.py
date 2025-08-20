# financial/views.py

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import FinancialProfile, Income, Expense, Debt, Asset, RiskAssessmentHistory
from .serializers import (
    FinancialProfileSerializer, FinancialProfileSummarySerializer,
    IncomeSerializer, IncomeCreateSerializer,
    ExpenseSerializer, ExpenseCreateSerializer,
    DebtSerializer, DebtCreateSerializer,
    AssetSerializer, AssetCreateSerializer,
    RiskAssessmentHistorySerializer, RiskAssessmentCreateSerializer
)


# FinancialProfile Views
class FinancialProfileListCreateView(generics.ListCreateAPIView):
    serializer_class = FinancialProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FinancialProfile.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FinancialProfileSummarySerializer
        return FinancialProfileSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FinancialProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FinancialProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return get_object_or_404(FinancialProfile, user=self.request.user)


# Income Views
class IncomeListCreateView(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        return Income.objects.filter(profile=profile)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return IncomeCreateSerializer
        return IncomeSerializer
    
    def perform_create(self, serializer):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        serializer.save(profile=profile)


class IncomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        return Income.objects.filter(profile=profile)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return IncomeCreateSerializer
        return IncomeSerializer


# Expense Views
class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        return Expense.objects.filter(profile=profile)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExpenseCreateSerializer
        return ExpenseSerializer
    
    def perform_create(self, serializer):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        serializer.save(profile=profile)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        return Expense.objects.filter(profile=profile)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ExpenseCreateSerializer
        return ExpenseSerializer


# Debt Views
class DebtListCreateView(generics.ListCreateAPIView):
    serializer_class = DebtSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        return Debt.objects.filter(profile=profile)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DebtCreateSerializer
        return DebtSerializer
    
    def perform_create(self, serializer):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        serializer.save(profile=profile)


class DebtDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DebtSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        return Debt.objects.filter(profile=profile)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return DebtCreateSerializer
        return DebtSerializer


# Asset Views
class AssetListCreateView(generics.ListCreateAPIView):
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        return Asset.objects.filter(profile=profile)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AssetCreateSerializer
        return AssetSerializer
    
    def perform_create(self, serializer):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        serializer.save(profile=profile)


class AssetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        return Asset.objects.filter(profile=profile)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AssetCreateSerializer
        return AssetSerializer


# Risk Assessment Views
class RiskAssessmentListCreateView(generics.ListCreateAPIView):
    serializer_class = RiskAssessmentHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        return RiskAssessmentHistory.objects.filter(profile=profile)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RiskAssessmentCreateSerializer
        return RiskAssessmentHistorySerializer
    
    def perform_create(self, serializer):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        serializer.save(profile=profile)


class RiskAssessmentDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = RiskAssessmentHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        profile = get_object_or_404(FinancialProfile, user=self.request.user)
        return RiskAssessmentHistory.objects.filter(profile=profile)


# Custom API Views
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def financial_summary(request):
    """Get a complete financial summary for the authenticated user"""
    try:
        profile = FinancialProfile.objects.get(user=request.user)
        
        summary_data = {
            'profile_id': profile.id,
            'user': profile.user.username,
            'last_assessed': profile.last_assessed,
            'financial_metrics': {
                'total_monthly_income': profile.get_total_income(),
                'total_monthly_expenses': profile.get_total_expenses(),
                'total_debt_balance': profile.get_total_debt_balance(),
                'total_assets_value': profile.get_total_assets_value(),
                'net_worth': profile.get_net_worth(),
                'debt_to_income_ratio': profile.get_debt_to_income_ratio(),
            },
            'counts': {
                'income_sources': profile.incomes.count(),
                'expense_categories': profile.expenses.count(),
                'debts': profile.debts.count(),
                'assets': profile.assets.count(),
                'risk_assessments': profile.risk_assessments.count(),
            },
            'latest_risk_assessment': {
                'score': profile.get_latest_risk_score(),
                'level': profile.risk_assessments.first().get_risk_level_display() if profile.risk_assessments.first() else None,
                'color': profile.risk_assessments.first().get_risk_level_display_color() if profile.risk_assessments.first() else None,
            },
            'profile_completeness': {
                'is_complete': profile.has_complete_profile(),
                'has_income': profile.incomes.exists(),
                'has_expenses': profile.expenses.exists(),
                'has_debts': profile.debts.exists(),
                'has_assets': profile.assets.exists(),
            }
        }
        
        return Response(summary_data, status=status.HTTP_200_OK)
    
    except FinancialProfile.DoesNotExist:
        return Response(
            {'error': 'Financial profile not found. Please create one first.'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bulk_create_financial_data(request):
    """Bulk create financial data in a single transaction"""
    try:
        profile = get_object_or_404(FinancialProfile, user=request.user)
        data = request.data
        
        with transaction.atomic():
            results = {
                'incomes_created': 0,
                'expenses_created': 0,
                'debts_created': 0,
                'assets_created': 0,
                'errors': []
            }
            
            # Create incomes
            if 'incomes' in data:
                for income_data in data['incomes']:
                    serializer = IncomeCreateSerializer(data=income_data)
                    if serializer.is_valid():
                        serializer.save(profile=profile)
                        results['incomes_created'] += 1
                    else:
                        results['errors'].append({'income': serializer.errors})
            
            # Create expenses
            if 'expenses' in data:
                for expense_data in data['expenses']:
                    serializer = ExpenseCreateSerializer(data=expense_data)
                    if serializer.is_valid():
                        serializer.save(profile=profile)
                        results['expenses_created'] += 1
                    else:
                        results['errors'].append({'expense': serializer.errors})
            
            # Create debts
            if 'debts' in data:
                for debt_data in data['debts']:
                    serializer = DebtCreateSerializer(data=debt_data)
                    if serializer.is_valid():
                        serializer.save(profile=profile)
                        results['debts_created'] += 1
                    else:
                        results['errors'].append({'debt': serializer.errors})
            
            # Create assets
            if 'assets' in data:
                for asset_data in data['assets']:
                    serializer = AssetCreateSerializer(data=asset_data)
                    if serializer.is_valid():
                        serializer.save(profile=profile)
                        results['assets_created'] += 1
                    else:
                        results['errors'].append({'asset': serializer.errors})
            
            return Response(results, status=status.HTTP_201_CREATED)
    
    except FinancialProfile.DoesNotExist:
        return Response(
            {'error': 'Financial profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )