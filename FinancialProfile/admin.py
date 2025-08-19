# financial/admin.py

from django.contrib import admin
from .models import FinancialProfile, Income, Expense, Debt, Asset, RiskAssessmentHistory


class IncomeInline(admin.TabularInline):
    model = Income
    extra = 1
    fields = ['source_name', 'amount', 'frequency']


class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 1
    fields = ['category', 'amount', 'frequency']


class DebtInline(admin.TabularInline):
    model = Debt
    extra = 1
    fields = ['debt_name', 'debt_type', 'remaining_balance', 'minimum_amount', 'interest_rate']


class AssetInline(admin.TabularInline):
    model = Asset
    extra = 1
    fields = ['asset_name', 'asset_type', 'value']


class RiskAssessmentInline(admin.TabularInline):
    model = RiskAssessmentHistory
    extra = 0
    readonly_fields = ['assessment_date', 'risk_level']
    fields = ['score', 'risk_level', 'assessment_date', 'summary']


@admin.register(FinancialProfile)
class FinancialProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'last_assessed', 'get_latest_risk_score', 'get_total_income', 'get_net_worth', 'created_at']
    list_filter = ['last_assessed', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'get_total_income', 'get_total_expenses', 'get_net_worth', 'get_debt_to_income_ratio']
    
    inlines = [IncomeInline, ExpenseInline, DebtInline, AssetInline, RiskAssessmentInline]
    
    fieldsets = (
        ('Profile Information', {
            'fields': ('user', 'last_assessed')
        }),
        ('Financial Summary', {
            'fields': ('get_total_income', 'get_total_expenses', 'get_net_worth', 'get_debt_to_income_ratio'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_latest_risk_score(self, obj):
        score = obj.get_latest_risk_score()
        return score if score is not None else 'Not assessed'
    get_latest_risk_score.short_description = 'Latest Risk Score'


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['source_name', 'amount', 'frequency', 'profile', 'created_at']
    list_filter = ['frequency', 'created_at']
    search_fields = ['source_name', 'profile__user__username']
    ordering = ['-created_at']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['category', 'amount', 'frequency', 'profile', 'created_at']
    list_filter = ['category', 'frequency', 'created_at']
    search_fields = ['category', 'profile__user__username']
    ordering = ['-created_at']


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ['debt_name', 'debt_type', 'remaining_balance', 'interest_rate', 'profile', 'created_at']
    list_filter = ['debt_type', 'created_at']
    search_fields = ['debt_name', 'profile__user__username']
    ordering = ['-created_at']
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['created_at', 'updated_at']
        if obj:  # Editing existing object
            readonly_fields.append('total_amount')
        return readonly_fields


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_name', 'asset_type', 'value', 'profile', 'created_at']
    list_filter = ['asset_type', 'created_at']
    search_fields = ['asset_name', 'profile__user__username']
    ordering = ['-created_at']


@admin.register(RiskAssessmentHistory)
class RiskAssessmentHistoryAdmin(admin.ModelAdmin):
    list_display = ['profile', 'score', 'risk_level', 'assessment_date']
    list_filter = ['risk_level', 'assessment_date']
    search_fields = ['profile__user__username']
    readonly_fields = ['assessment_date', 'risk_level']
    ordering = ['-assessment_date']
    
    def has_add_permission(self, request):
        # Risk assessments should be created through the API, not admin
        return False