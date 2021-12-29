class Eva():
    def __init__(self):
        print("will have stuff soon")

    def eval(self, exp):
        if self._isNumber(exp):
            return exp

        if self._isString(exp):
            return exp

        if exp[0] == '+':
            return self.eval(exp[1]) + self.eval(exp[2]);

        if exp[0] == '*':
            return self.eval(exp[1]) * self.eval(exp[2]);

        # reached the bottom of eval
        return "No such luck"

    def _isNumber(self, exp):
        return type(exp) in [int, float]

    def _isString(self, exp):
        return type(exp) in [str]
