import unittest
from payroll.factory import Factory


class TestFactory(unittest.TestCase):

    def test_no_name(self):
        with self.assertRaises(ValueError):
            Factory.build_payee()

    def test_no_base_pay(self):
        with self.assertRaises(ValueError):
            Factory.build_payee(name="Test")

    def test_salaried_no_deductions(self):
        payee = Factory.build_payee(name="Salaried", base_pay=4200)
        self.assertEqual("Salaried", payee.name)
        self.assertEqual(4200, payee.base_pay)
        self.assertEqual(4200, payee.take_home_pay)
        print(payee)

    def test_hourly_without_hours_provided_exception(self):
        with self.assertRaises(ValueError):
            payee = Factory.build_payee(name="Test", base_pay=600, hourly=True)

    def test_hourly_exempt(self):
        payee = Factory.build_payee(name="Hourly Exempt", base_pay=600, hourly=True, hours_worked=50)
        self.assertEqual(750, payee.take_home_pay)
        print(payee)

    def test_hourly_overtime(self):
        payee = Factory.build_payee(name="Hourly Overtime", base_pay=600, hourly=True, exempt=False, hours_worked=50)
        self.assertEqual(975, payee.take_home_pay)
        print(payee)

    def test_commission_without_total_sales_provided(self):
        with self.assertRaises(ValueError):
            payee = Factory.build_payee(name="Salaried", base_pay=2000, commission=True)

    def test_salaried_with_sales_commission(self):
        payee = Factory.build_payee(name="Salaried Commissioned", base_pay=2000,
                                    commission=True, total_sales=10000)
        self.assertEqual(3000,payee.take_home_pay)
        print(payee)

    def test_hourly_with_sales_commission(self):
        payee = Factory.build_payee(name="Hourly Commissioned", base_pay=1000,  hourly=True, exempt=True, hours_worked=40,
                                    commission=True, total_sales=10000)
        self.assertEqual(2000, payee.take_home_pay)
        print(payee)

    def test_that_commissioned_must_be_exempt(self):
        with self.assertRaises(ValueError):
            payee = Factory.build_payee(name="Test", base_pay=1000,
                                        hourly=True, exempt=False, hours_worked=40,
                                        commission=True, total_sales=10000)

    def test_charity_without_tax_withholding(self):
        with self.assertRaises(ValueError):
            payee = Factory.build_payee(name="Salaried", base_pay=4200, charity=True)

    def test_retirement_savings_without_tax_withholding(self):
        with self.assertRaises(ValueError):
            payee = Factory.build_payee(name="Salaried", base_pay=4200, retirement_savings=True)

    def test_charity_without_donation(self):
        with self.assertRaises(ValueError):
            payee = Factory.build_payee(name="Charity", base_pay=4200,
                                        tax_withholding=True, charity=True)

    def test_salaried_with_tax_withholding(self):
        payee = Factory.build_payee(name="Salaried Taxed", base_pay=1000, tax_withholding=True)
        self.assertEqual(780, payee.take_home_pay)
        print(payee)

    def test_salaried_with_tax_withholding_and_retirement_savings(self):
        payee = Factory.build_payee(name="Retirement Savings", base_pay=1000, tax_withholding=True,
                                    retirement_savings=True)
        self.assertEqual(855, payee.take_home_pay)
        print(payee)

    def test_salaried_with_tax_withholding_and_charity_donation(self):
        payee = Factory.build_payee(name="Charitable Donation", base_pay=1000, tax_withholding=True,
                                    charity=True, donation=10)
        self.assertEqual(772.20, payee.take_home_pay)
        print(payee)

    def test_tax_with_retirement_savings_and_charity_donation(self):
        payee = Factory.build_payee(name="Charity and Savings", base_pay=1000, tax_withholding=True,
                                    charity=True, donation=10, retirement_savings=True)
        self.assertEqual(846.00, payee.take_home_pay)
        print(payee)

    def test_tax_with_retirement_savings_and_charity_donation_and_health_club(self):
        payee = Factory.build_payee(name="Health Club", base_pay=1000, health_club=True)
        self.assertEqual(1000-7.60, payee.take_home_pay)
        print(payee)
