def isBool(value):
    return value is not None and isinstance(value, bool)


def isNumberBetween(min, max):
    def isNumberBetween(value):
        if value is None or not isinstance(value, (int, float)):
            return False
        if value < min or value > max:
            return False
        return True

    return isNumberBetween


def isNumberBetweenZeroAndOne(value):
    return isNumberBetween(0, 1)(value)
