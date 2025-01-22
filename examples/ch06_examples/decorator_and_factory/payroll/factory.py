from payroll.employee import IPayable, Employee
from payroll.decorators import *


class Factory:

    @classmethod
    def build_payee(cls, name=None, base_pay=None, regular_hours=40,
                    hourly=False, exempt=True, hours_worked=None,
                    commission=False, total_sales=None, health_club=False,
                    tax_withholding=False, retirement_savings=False,
                    charity=False, donation=None):
        if name is None:
            raise ValueError("name cannot be None")
        if base_pay is None:
            raise ValueError("base_pay amount cannot be None")
        if commission and hourly and not exempt:
            raise ValueError("Hourly Commissioned must be exempt")
        if hourly and (hours_worked is None or hours_worked < 0):
            raise ValueError("hours_worked must be provided for hourly pay.")
        if not tax_withholding:
            if charity or retirement_savings:
                raise ValueError("Retirement savings and charity cannot be claimed without tax withholding")
        if charity and donation is None:
            raise ValueError("A donation amount must be given for charity deduction")

# Income decorators ----------------------------------------------------------------------------------------
        payee = Employee(name, base_pay, regular_hours)     # default is salaried employee

        if hourly:
            if exempt:
                payee = HourlyExempt(payee, hours_worked)
            else:
                payee = HourlyOvertime(payee, hours_worked)

        if commission:
            if total_sales is None:
                raise ValueError("total_sales ")
            payee = SalesCommission(payee, total_sales)


# Tax reduction decorators -----------------------------------------------------------------------------
        if retirement_savings:
            payee = RetirementSavings(payee)

        if charity:
            payee = CharityDonation(payee, donation)

# Tax withholding --------------------------------------------------------------------------------------
        if tax_withholding:
            payee = Taxes(payee)

# Post tax deductions to take home pay ------------------------------------------------------------------
        if health_club:
            payee = HealthClub(payee)

        return payee
