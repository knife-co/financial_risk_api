# Create a new app for financial models
# Run: python manage.py startapp financial

# financial/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.utils import timezone

User = get_user_model()


class FinancialProfile(models.Model):
    """
    Financial profile with one-to-one relationship to User
    Central model that connects to all financial data
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='financial_profile'
    )
    last_assessed = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Financial Profile"
        verbose_name_plural = "Financial Profiles"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Financial Profile for {self.user.username}"
    
    # Profile management methods

    def create_risk_assessment(self):
        """Create a new risk assessment for this profile"""
        from .risk_calculator import FinancialRiskCalculator  # Import here to avoid circular imports
        
        calculator = FinancialRiskCalculator(self)
        score = calculator.calculate_risk_score()
        summary = calculator.generate_risk_summary()
        
        assessment = RiskAssessmentHistory.objects.create(
            profile=self,
            score=score,
            summary=summary
        )
        
        return assessment

    def update_last_assessed(self):
        """Update the last assessment timestamp"""
        self.last_assessed = timezone.now()
        self.save(update_fields=['last_assessed'])
    
    def get_total_income(self):
        """Calculate total monthly income"""
        monthly_income = Decimal('0.00')
        for income in self.incomes.all():
            if income.frequency.lower() == 'monthly':
                monthly_income += income.amount
            elif income.frequency.lower() == 'yearly':
                monthly_income += income.amount / 12
            elif income.frequency.lower() == 'weekly':
                monthly_income += income.amount * 4
        return monthly_income
    
    def get_total_expenses(self):
        """Calculate total monthly expenses"""
        monthly_expenses = Decimal('0.00')
        for expense in self.expenses.all():
            if expense.frequency.lower() == 'monthly':
                monthly_expenses += expense.amount
            elif expense.frequency.lower() == 'yearly':
                monthly_expenses += expense.amount / 12
            elif expense.frequency.lower() == 'weekly':
                monthly_expenses += expense.amount * 4
        return monthly_expenses
    
    def get_total_debt_balance(self):
        """Calculate total remaining debt balance"""
        return sum(debt.remaining_balance for debt in self.debts.all())
    
    def get_total_assets_value(self):
        """Calculate total assets value"""
        return sum(asset.value for asset in self.assets.all())
    
    def get_net_worth(self):
        """Calculate net worth (assets - debts)"""
        return self.get_total_assets_value() - self.get_total_debt_balance()
    
    def get_debt_to_income_ratio(self):
        """Calculate debt-to-income ratio"""
        total_income = self.get_total_income()
        if total_income > 0:
            total_debt_payments = sum(debt.minimum_amount for debt in self.debts.all())
            return (total_debt_payments / total_income) * 100
        return 0
    
    def get_latest_risk_score(self):
        """Get the most recent risk assessment score"""
        latest_assessment = self.risk_assessments.first()
        return latest_assessment.score if latest_assessment else None
    
    def has_complete_profile(self):
        """Check if profile has minimum required data for assessment"""
        return (
            self.incomes.exists() and
            self.expenses.exists() and
            (self.debts.exists() or self.assets.exists())
        )


class Income(models.Model):
    """
    Income sources for a financial profile
    """
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('bi_weekly', 'Bi-Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name='incomes'
    )
    source_name = models.CharField(max_length=100)
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.source_name}: ${self.amount} ({self.frequency})"
    
    def get_monthly_amount(self):
        """Convert any frequency to monthly amount"""
        if self.frequency == 'weekly':
            return self.amount * 4
        elif self.frequency == 'bi_weekly':
            return self.amount * 2
        elif self.frequency == 'monthly':
            return self.amount
        elif self.frequency == 'quarterly':
            return self.amount / 3
        elif self.frequency == 'yearly':
            return self.amount / 12
        return self.amount


class Expense(models.Model):
    """
    Expenses for a financial profile
    """
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('bi_weekly', 'Bi-Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    CATEGORY_CHOICES = [
        ('housing', 'Housing'),
        ('transportation', 'Transportation'),
        ('food', 'Food & Dining'),
        ('utilities', 'Utilities'),
        ('healthcare', 'Healthcare'),
        ('entertainment', 'Entertainment'),
        ('education', 'Education'),
        ('insurance', 'Insurance'),
        ('debt_payments', 'Debt Payments'),
        ('savings', 'Savings'),
        ('other', 'Other'),
    ]
    
    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_category_display()}: ${self.amount} ({self.frequency})"
    
    def get_monthly_amount(self):
        """Convert any frequency to monthly amount"""
        if self.frequency == 'weekly':
            return self.amount * 4
        elif self.frequency == 'bi_weekly':
            return self.amount * 2
        elif self.frequency == 'monthly':
            return self.amount
        elif self.frequency == 'quarterly':
            return self.amount / 3
        elif self.frequency == 'yearly':
            return self.amount / 12
        return self.amount


class Debt(models.Model):
    """
    Debt information for a financial profile
    """
    DEBT_TYPE_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('student_loan', 'Student Loan'),
        ('mortgage', 'Mortgage'),
        ('auto_loan', 'Auto Loan'),
        ('personal_loan', 'Personal Loan'),
        ('medical_debt', 'Medical Debt'),
        ('other', 'Other'),
    ]
    
    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name='debts'
    )
    debt_name = models.CharField(max_length=100)
    debt_type = models.CharField(max_length=20, choices=DEBT_TYPE_CHOICES, default='other')
    total_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    remaining_balance = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    minimum_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    interest_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.debt_name}: ${self.remaining_balance} remaining"
    
    def get_debt_ratio(self):
        """Calculate what percentage of original debt remains"""
        if self.total_amount > 0:
            return (self.remaining_balance / self.total_amount) * 100
        return 0
    
    def is_high_interest(self):
        """Check if debt has high interest rate (>15%)"""
        return self.interest_rate > 15


class Asset(models.Model):
    """
    Assets for a financial profile
    """
    ASSET_TYPE_CHOICES = [
        ('checking', 'Checking Account'),
        ('savings', 'Savings Account'),
        ('investment', 'Investment Account'),
        ('retirement', 'Retirement Account'),
        ('real_estate', 'Real Estate'),
        ('vehicle', 'Vehicle'),
        ('cryptocurrency', 'Cryptocurrency'),
        ('precious_metals', 'Precious Metals'),
        ('business', 'Business Assets'),
        ('other', 'Other'),
    ]
    
    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name='assets'
    )
    asset_name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPE_CHOICES)
    value = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.asset_name}: ${self.value}"
    
    def is_liquid_asset(self):
        """Check if asset is easily convertible to cash"""
        liquid_types = ['checking', 'savings', 'investment']
        return self.asset_type in liquid_types


class RiskAssessmentHistory(models.Model):
    """
    Historical risk assessment scores and summaries
    """
    RISK_LEVEL_CHOICES = [
        ('very_low', 'Very Low Risk'),
        ('low', 'Low Risk'),
        ('moderate', 'Moderate Risk'),
        ('high', 'High Risk'),
        ('very_high', 'Very High Risk'),
    ]
    
    profile = models.ForeignKey(
        FinancialProfile,
        on_delete=models.CASCADE,
        related_name='risk_assessments'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, blank=True)
    assessment_date = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Risk Assessment History"
        verbose_name_plural = "Risk Assessment Histories"
        ordering = ['-assessment_date']
    
    def __str__(self):
        return f"Risk Assessment {self.score} for {self.profile.user.username} on {self.assessment_date.date()}"
    
    def save(self, *args, **kwargs):
        """Automatically set risk level based on score"""
        if not self.risk_level:
            if self.score <= 20:
                self.risk_level = 'very_low'
            elif self.score <= 40:
                self.risk_level = 'low'
            elif self.score <= 60:
                self.risk_level = 'moderate'
            elif self.score <= 80:
                self.risk_level = 'high'
            else:
                self.risk_level = 'very_high'
        
        super().save(*args, **kwargs)
        
        # Update the profile's last_assessed timestamp
        self.profile.update_last_assessed()
    
    def get_risk_level_display_color(self):
        """Return color code for frontend display"""
        colors = {
            'very_low': '#22c55e',    # Green
            'low': '#84cc16',         # Light green
            'moderate': '#eab308',    # Yellow
            'high': '#f97316',        # Orange
            'very_high': '#ef4444',   # Red
        }
        return colors.get(self.risk_level, '#6b7280')  # Default gray

        
    