from abc import ABCMeta, abstractmethod

"""
IPayable interface for decorator construction sample
"""


class IPayable(metaclass=ABCMeta):
    """ Interface for any object that can be paid including Employee. """

    @abstractmethod
    def base_pay(self):
        """ Payee weekly base pay """

    @abstractmethod
    def regular_hours(self):
        """ Regular weekly hours """

    @abstractmethod
    def take_home_pay(self):
        """ Calculated take home pay after deductions """

    @abstractmethod
    def name(self):
        """ Name of payee """


class Employee(IPayable):
    def __init__(self, name, base_pay, regular_hours=40):
        super().__init__()
        self._name = name
        self._base_pay = base_pay
        self._regular_hours = regular_hours

    @property
    def name(self):
        return self._name

    @property
    def base_pay(self):
        return self._base_pay

    @property
    def regular_hours(self):
        return self._regular_hours

    @property
    def take_home_pay(self):
        return self._base_pay

    def __str__(self):
        return f'{self.name:20}  {self.take_home_pay: 9.2f} base pay for {self.regular_hours} regular hours'
