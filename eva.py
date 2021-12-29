import re

from environment import Environment

class Eva():
    def __init__(self):
        pass

    def eval(self, exp, env):
        if self._isNumber(exp, env):
            return exp

        if self._isString(exp, env):
            return exp

        if self._isSymbol(exp, env):
            return env.lookup(exp)

        # Basic math
        if exp[0] == '+':
            return self.eval(exp[1], env) + self.eval(exp[2], env);

        if exp[0] == '-':
            return self.eval(exp[1], env) - self.eval(exp[2], env);

        if exp[0] == '*':
            return self.eval(exp[1], env) * self.eval(exp[2], env);

        if exp[0] == '/':
            return self.eval(exp[1], env) / self.eval(exp[2], env);

        # Blocks
        if exp[0] == 'begin':
            blockEnv = Environment({}, env);
            result = None
            for expression in exp[1:]:
                result = self.eval(expression, blockEnv)
            return result

        # Variables
        if exp[0] == 'var':
            [_, name, value] = exp
            return env.define(name, value)



        # reached the bottom of eval
        raise ValueError('expression not found: ', exp);


    def _isNumber(self, exp, env):
        return type(exp) in [int, float]

    def _isString(self, exp, env):
        if type(exp) != str:
            return False
        pattern = '^\"(.*?)\"$'
        return re.match(pattern, exp)

    def _isSymbol(self, exp, env):
        return type(exp) in [str]
