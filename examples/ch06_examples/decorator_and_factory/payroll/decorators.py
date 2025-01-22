from payroll.employee import IPayable

"""
Decorators for various pay options for different types of employee
Note that the print statements and initialization of basic employee
information would not be necessary.
"""


class Decorator(IPayable):

    @property
    def take_home_pay(self):
        pass

    @property
    def name(self):
        return self.employee.name

    @property
    def regular_hours(self):
        return self.employee.regular_hours

    @property
    def base_pay(self):
        return self.employee.base_pay


class HourlyExempt(Decorator):
    def __init__(self, employee, hours_worked):
        super().__init__()
        self.employee = employee
        self.hours_worked = hours_worked

    @property
    def take_home_pay(self):
        hourly_rate = self.base_pay / self.regular_hours
        return hourly_rate * self.hours_worked

    def __str__(self):
        return f'{self.name:20}  {self.take_home_pay: 9.2f} weekly earnings for {self.hours_worked} hours work (exempt)'


class HourlyOvertime(Decorator):
    def __init__(self, employee, hours_worked):
        super().__init__()
        self.employee = employee
        self.hours_worked = hours_worked

    @property
    def take_home_pay(self):
        hourly_rate = self.base_pay / self.regular_hours
        pay = hourly_rate * self.hours_worked
        if self.hours_worked > self.regular_hours:
            extra_hours = self.hours_worked - self.regular_hours
            pay += extra_hours * hourly_rate * 1.5
        return pay

    def __str__(self):
        return f'{self.name:20}  {self.take_home_pay: 9.2f} weekly earnings for {self.hours_worked} hours worked (overtime)'


class SalesCommission(Decorator):
    def __init__(self, employee, total_sales):
        self.employee = employee
        self.total_sales = total_sales

    @property
    def take_home_pay(self):
        return self.employee.take_home_pay + self.total_sales * .10

    def __str__(self):
        return f'{self.name:20}  {self.take_home_pay: 9.2f} with commission for {self.total_sales} in total sales'


class RetirementSavings(Decorator):
    def __init__(self, employee):
        self.employee = employee

    @property
    def take_home_pay(self):
        return self.employee.take_home_pay - (self.employee.take_home_pay * .05)

    def __str__(self):
        return f'{self.name:20}  {self.take_home_pay: 9.2f} retirement savings'


class CharityDonation(Decorator):
    def __init__(self, employee, donation):
        self.employee = employee
        self.donation = donation

    @property
    def take_home_pay(self):
        return self.employee.take_home_pay - self.donation

    def __str__(self):
        return f'{self.name:20}  {self.take_home_pay: 9.2f} after donating {self.donation:.2f} to charity'


class Taxes(Decorator):
    def __init__(self, employee):
        self.employee = employee
        self.tax_withholding = 0.0

    @property
    def take_home_pay(self):
        estimate = self.employee.take_home_pay * 52
        rate = 0.
        if estimate > 250000:
            rate = .45
        elif estimate > 200000:
            rate = .4
        elif estimate > 150000:
            rate = .35
        elif estimate > 100000:
            rate = .3
        elif estimate > 50000:
            rate = .22
        elif estimate > 30000:
            rate = .10

        self.tax_withholding = self.employee.take_home_pay * rate
        return self.employee.take_home_pay - self.tax_withholding

    def __str__(self):
        return f'{self.name:20}  {self.take_home_pay: 9.2f} after paying {self.tax_withholding:.2f} in taxes'


class HealthClub(Decorator):
    def __init__(self, employee):
        self.employee = employee
        self.membership_fee = 7.60

    @property
    def take_home_pay(self):
        return self.employee.take_home_pay - self.membership_fee

    def __str__(self):
        return f'{self.name:20}  {self.take_home_pay: 9.2f} after paying {self.membership_fee:.2f} health club dues'
