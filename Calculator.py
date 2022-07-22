class Calculator:
    def add(self, first, second):
        return first + second

    def subtract(self, first, second):
        return first - second

    def multiply(self, first, second):
        return first * second

    def divide(self, first, second):
        if second == 0:
            raise Exception("Second value can't be 0.")
        else:
            return first / second

    def mod(self, first, second):
        if second == 0:
            raise Exception("Second value can't be 0.")
        else:
            return first % second
