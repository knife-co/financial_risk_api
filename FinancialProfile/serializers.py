# FinancialProfile/serializers.py

from rest_framework import serializers
from .models import FinancialProfile, Income, Expense, Debt, Asset, RiskAssessmentHistory
from django.contrib.auth import get_user_model

User = get_user_model()


class IncomeSerializer(serializers.ModelSerializer):
    monthly_amount = serializers.ReadOnlyField(source='get_monthly_amount')
    
    class Meta:
        model = Income
        fields = ['id', 'source_name', 'amount', 'frequency', 'monthly_amount', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'monthly_amount']


class ExpenseSerializer(serializers.ModelSerializer):
    monthly_amount = serializers.ReadOnlyField(source='get_monthly_amount')
    category_display = serializers.ReadOnlyField(source='get_category_display')
    
    class Meta:
        model = Expense
        fields = ['id', 'category', 'category_display', 'amount', 'frequency', 'monthly_amount', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'monthly_amount', 'category_display']


class DebtSerializer(serializers.ModelSerializer):
    debt_type_display = serializers.ReadOnlyField(source='get_debt_type_display')
    debt_ratio = serializers.ReadOnlyField(source='get_debt_ratio')
    is_high_interest = serializers.ReadOnlyField()
    
    class Meta:
        model = Debt
        fields = [
            'id', 'debt_name', 'debt_type', 'debt_type_display', 
            'total_amount', 'remaining_balance', 'minimum_amount', 
            'interest_rate', 'debt_ratio', 'is_high_interest',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'debt_type_display', 'debt_ratio', 'is_high_interest']
    
    def validate(self, data):
        """Ensure remaining balance doesn't exceed total amount"""
        if 'remaining_balance' in data and 'total_amount' in data:
            if data['remaining_balance'] > data['total_amount']:
                raise serializers.ValidationError(
                    "Remaining balance cannot exceed total amount"
                )
        return data


class AssetSerializer(serializers.ModelSerializer):
    asset_type_display = serializers.ReadOnlyField(source='get_asset_type_display')
    is_liquid = serializers.ReadOnlyField(source='is_liquid_asset')
    
    class Meta:
        model = Asset
        fields = [
            'id', 'asset_name', 'asset_type', 'asset_type_display', 
            'value', 'is_liquid', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'asset_type_display', 'is_liquid']


class RiskAssessmentHistorySerializer(serializers.ModelSerializer):
    risk_level_display = serializers.ReadOnlyField(source='get_risk_level_display')
    risk_color = serializers.ReadOnlyField(source='get_risk_level_display_color')
    
    class Meta:
        model = RiskAssessmentHistory
        fields = [
            'id', 'score', 'risk_level', 'risk_level_display', 
            'risk_color', 'assessment_date', 'summary'
        ]
        read_only_fields = ['id', 'risk_level', 'assessment_date', 'risk_level_display', 'risk_color']


class FinancialProfileSerializer(serializers.ModelSerializer):
    # Nested relationships
    incomes = IncomeSerializer(many=True, read_only=True)
    expenses = ExpenseSerializer(many=True, read_only=True)
    debts = DebtSerializer(many=True, read_only=True)
    assets = AssetSerializer(many=True, read_only=True)
    risk_assessments = RiskAssessmentHistorySerializer(many=True, read_only=True)
    
    # Calculated fields
    total_income = serializers.ReadOnlyField(source='get_total_income')
    total_expenses = serializers.ReadOnlyField(source='get_total_expenses')
    total_debt_balance = serializers.ReadOnlyField(source='get_total_debt_balance')
    total_assets_value = serializers.ReadOnlyField(source='get_total_assets_value')
    net_worth = serializers.ReadOnlyField(source='get_net_worth')
    debt_to_income_ratio = serializers.ReadOnlyField(source='get_debt_to_income_ratio')
    latest_risk_score = serializers.ReadOnlyField(source='get_latest_risk_score')
    has_complete_profile = serializers.ReadOnlyField()
    
    # User information
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = FinancialProfile
        fields = [
            'id', 'user', 'username', 'last_assessed', 
            'total_income', 'total_expenses', 'total_debt_balance', 
            'total_assets_value', 'net_worth', 'debt_to_income_ratio',
            'latest_risk_score', 'has_complete_profile',
            'incomes', 'expenses', 'debts', 'assets', 'risk_assessments',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'username', 'last_assessed', 'created_at', 'updated_at',
            'total_income', 'total_expenses', 'total_debt_balance', 
            'total_assets_value', 'net_worth', 'debt_to_income_ratio',
            'latest_risk_score', 'has_complete_profile',
            'incomes', 'expenses', 'debts', 'assets', 'risk_assessments'
        ]


class FinancialProfileSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    total_income = serializers.ReadOnlyField(source='get_total_income')
    net_worth = serializers.ReadOnlyField(source='get_net_worth')
    latest_risk_score = serializers.ReadOnlyField(source='get_latest_risk_score')
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = FinancialProfile
        fields = [
            'id', 'username', 'last_assessed', 'total_income', 
            'net_worth', 'latest_risk_score', 'created_at'
        ]


# Nested serializers for creating related objects
class IncomeCreateSerializer(serializers.ModelSerializer):
    frequency = serializers.ChoiceField(choices=Income.FREQUENCY_CHOICES, required = True)
    class Meta:
        model = Income
        fields = ['source_name', 'amount', 'frequency']


class ExpenseCreateSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Expense.CATEGORY_CHOICES, required=True)
    frequency = serializers.ChoiceField(choices=Expense.FREQUENCY_CHOICES, required=True)
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'frequency']


class DebtCreateSerializer(serializers.ModelSerializer):
    debt_type = serializers.ChoiceField(choices=Debt.DEBT_TYPE_CHOICES, required=True)
    class Meta:
        model = Debt
        fields = ['debt_name', 'debt_type', 'total_amount', 'remaining_balance', 'minimum_amount', 'interest_rate']
    
    def validate(self, data):
        if data['remaining_balance'] > data['total_amount']:
            raise serializers.ValidationError(
                "Remaining balance cannot exceed total amount"
            )
        return data


class AssetCreateSerializer(serializers.ModelSerializer):
    asset_type = serializers.ChoiceField(choices=Asset.ASSET_TYPE_CHOICES)
    class Meta:
        model = Asset
        fields = ['asset_name', 'asset_type', 'value']


class RiskAssessmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskAssessmentHistory
        fields = ['score', 'summary']