"""debugging_demo.py - Example of debugging from chapter 4"""


class DebuggingDemo:

    def __init__(self, name, num_loops):
        self._name = name
        self._count = num_loops

    def count(self):
        i = -1
        for i in range(self._count):
            print(i)
        return f'{self._name} executed {i+1} of {self._count} loops'


if __name__ == '__main__':
    obj_name = 'debugging demo'
    print('Starting ' + obj_name + '...')
    pd = DebuggingDemo(obj_name, 5)
    result = pd.count()
    print(result)
