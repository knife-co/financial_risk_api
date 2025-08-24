# financial/risk_calculator.py

from decimal import Decimal


class FinancialRiskCalculator:
    """
    Calculate financial risk score based on various factors
    Score ranges from 0-100 (higher = more risk)
    """
    
    def __init__(self, profile):
        self.profile = profile
        self.risk_factors = {}
        self.total_score = 0
    
    def calculate_risk_score(self):
        """Main method to calculate overall risk score"""
        self.risk_factors = {
            'debt_to_income_ratio': self._calculate_debt_ratio_risk(),
            'emergency_fund_ratio': self._calculate_emergency_fund_risk(),
            'high_interest_debt': self._calculate_high_interest_debt_risk(),
            'income_stability': self._calculate_income_stability_risk(),
            'expense_coverage': self._calculate_expense_coverage_risk(),
            'debt_diversity': self._calculate_debt_diversity_risk(),
        }
        
        # Weighted average of risk factors
        weights = {
            'debt_to_income_ratio': 0.25,      # 25%
            'emergency_fund_ratio': 0.20,      # 20%
            'high_interest_debt': 0.20,        # 20%
            'income_stability': 0.15,          # 15%
            'expense_coverage': 0.15,          # 15%
            'debt_diversity': 0.05,            # 5%
        }
        
        weighted_score = sum(
            self.risk_factors[factor] * weights[factor] 
            for factor in weights
        )
        
        self.total_score = min(100, max(0, int(weighted_score)))
        return self.total_score
    
    def _calculate_debt_ratio_risk(self):
        """Calculate risk based on debt-to-income ratio"""
        ratio = self.profile.get_debt_to_income_ratio()
        
        if ratio == 0:
            return 0  # No debt = no risk
        elif ratio <= 20:
            return 10  # Very low risk
        elif ratio <= 36:
            return 25  # Acceptable risk
        elif ratio <= 50:
            return 60  # High risk
        else:
            return 90  # Very high risk
    
    def _calculate_emergency_fund_risk(self):
        """Calculate risk based on emergency fund coverage"""
        monthly_expenses = self.profile.get_total_expenses()
        liquid_assets = sum(
            asset.value for asset in self.profile.assets.all() 
            if asset.is_liquid_asset()
        )
        
        if monthly_expenses == 0:
            return 0
        
        months_covered = liquid_assets / monthly_expenses if monthly_expenses > 0 else 0
        
        if months_covered >= 6:
            return 5   # Excellent emergency fund
        elif months_covered >= 3:
            return 20  # Good emergency fund
        elif months_covered >= 1:
            return 50  # Minimal emergency fund
        else:
            return 85  # No emergency fund
    
    def _calculate_high_interest_debt_risk(self):
        """Calculate risk based on high-interest debt"""
        total_debt = self.profile.get_total_debt_balance()
        if total_debt == 0:
            return 0
        
        high_interest_debt = sum(
            debt.remaining_balance for debt in self.profile.debts.all()
            if debt.is_high_interest()
        )
        
        high_interest_ratio = (high_interest_debt / total_debt) * 100
        
        if high_interest_ratio == 0:
            return 5
        elif high_interest_ratio <= 25:
            return 30
        elif high_interest_ratio <= 50:
            return 60
        else:
            return 90
    
    def _calculate_income_stability_risk(self):
        """Calculate risk based on income source diversity"""
        income_sources = self.profile.incomes.count()
        
        if income_sources == 0:
            return 100  # No income = maximum risk
        elif income_sources == 1:
            return 70   # Single income source = high risk
        elif income_sources == 2:
            return 40   # Two sources = moderate risk
        else:
            return 15   # Multiple sources = low risk
    
    def _calculate_expense_coverage_risk(self):
        """Calculate risk based on income vs expenses"""
        total_income = self.profile.get_total_income()
        total_expenses = self.profile.get_total_expenses()
        
        if total_income == 0:
            return 100
        
        coverage_ratio = (total_expenses / total_income) * 100
        
        if coverage_ratio <= 50:
            return 5   # Saving 50%+ of income
        elif coverage_ratio <= 80:
            return 20  # Saving 20%+ of income
        elif coverage_ratio <= 100:
            return 50  # Breaking even
        else:
            return 95  # Spending more than earning
    
    def _calculate_debt_diversity_risk(self):
        """Calculate risk based on debt type diversity"""
        debt_types = set(debt.debt_type for debt in self.profile.debts.all())
        debt_count = len(debt_types)
        
        if debt_count == 0:
            return 0
        elif debt_count <= 2:
            return 20
        elif debt_count <= 4:
            return 50
        else:
            return 80  # Too many different debt types
    
    def generate_risk_summary(self):
        """Generate a text summary of the risk assessment"""
        score = self.calculate_risk_score()
        
        summary_parts = []
        
        # Overall risk level
        if score <= 20:
            summary_parts.append("Your financial risk is very low. You have excellent financial health.")
        elif score <= 40:
            summary_parts.append("Your financial risk is low. You have good financial stability.")
        elif score <= 60:
            summary_parts.append("Your financial risk is moderate. There are areas for improvement.")
        elif score <= 80:
            summary_parts.append("Your financial risk is high. Consider addressing key issues.")
        else:
            summary_parts.append("Your financial risk is very high. Immediate action recommended.")
        
        # Specific recommendations
        if self.risk_factors.get('debt_to_income_ratio', 0) > 50:
            summary_parts.append("Consider reducing debt payments or increasing income.")
        
        if self.risk_factors.get('emergency_fund_ratio', 0) > 70:
            summary_parts.append("Build an emergency fund covering 3-6 months of expenses.")
        
        if self.risk_factors.get('high_interest_debt', 0) > 60:
            summary_parts.append("Focus on paying down high-interest debt first.")
        
        if self.risk_factors.get('expense_coverage', 0) > 70:
            summary_parts.append("Review expenses and create a budget to live within your means.")
        
        return " ".join(summary_parts)