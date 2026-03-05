import math

def analyze(x):
    if x > 0:
        if x % 2 == 0:
            if x > 100:
                return 1
            elif x > 50:
                return 2
            else:
                return 3
        else:
            if x > 75:
                return 4
            elif x > 25:
                return 5
            else:
                return 6
    elif x == 0:
        return 7
    else:
        if x < -100:
            return 8
        elif x < -50:
            return 9
        elif x < -10:
            return 10
        else:
            return 11

