from payroll.decorators import *
from payroll.employee import *


if __name__ == '__main__':
    payee = Employee("Flintstone, Fred J.", 600)
    print(payee)
    payee = HourlyOvertime(payee, 50)
    print(payee)
