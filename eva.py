import re

from environment import Environment
from parser import Parser
from transformer import Transformer

parser = Parser()
transformer = Transformer()

class Eva():
    def __init__(self):
        pass

    def evalNew(self, input):
        def square(x):
            return x * x

        def sum(a, b):
            return a + b
        ast = parser.parse(input)
        globalEnv = Environment({
            'version': 1.0,
            'square': square,
            'sum': sum
        }, None);
        return self.eval(ast, globalEnv)

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

        # Comparisons
        if exp[0] == '=':
            return self.eval(exp[1], env) == self.eval(exp[2], env);

        if exp[0] == '<>':
            return self.eval(exp[1], env) != self.eval(exp[2], env);

        if exp[0] == '<=':
            return self.eval(exp[1], env) <= self.eval(exp[2], env);

        if exp[0] == '>=':
            return self.eval(exp[1], env) >= self.eval(exp[2], env);

        if exp[0] == '<':
            return self.eval(exp[1], env) < self.eval(exp[2], env);

        if exp[0] == '>':
            return self.eval(exp[1], env) > self.eval(exp[2], env);

        # Logical
        if exp[0] == 'and':
            return self.eval(exp[1], env) and self.eval(exp[2], env);

        if exp[0] == 'or':
            return self.eval(exp[1], env) or self.eval(exp[2], env);

        if exp[0] == 'not':
            return not self.eval(exp[1], env);

        if exp[0] == 'print':
            res = self.eval(exp[1], env)
            print(res)
            return res

        # Blocks
        if exp[0] == 'begin':
            blockEnv = Environment({}, env);
            result = None
            for expression in exp[1:]:
                result = self.eval(expression, blockEnv)
            return result

        # If statements
        if exp[0] == 'if':
            [_if, condition, consequent, alternative] = exp
            if self.eval(condition, env):
                return self.eval(consequent, env)
            else:
                return self.eval(alternative, env)

        # While statement
        if exp[0] == 'while':
            [_if, condition, body] = exp
            result = None
            while self.eval(condition, env):
                result = self.eval(body, env)
            return result

        # Variables
        if exp[0] == 'var':
            [_, name, value] = exp
            return env.define(name, self.eval(value, env))

        if exp[0] == 'set':
            [_, name, value] = exp
            return env.assign(name, self.eval(value, env))

        # Functions
        if exp[0] == 'lambda':
            [_, params, body] = exp;
            return { 'params': params, 'body': body, 'env': env }

        if exp[0] == 'def':
            varExp = transformer.transformDefToLambda(exp)
            return self.eval(varExp, env);

        if isinstance(exp, list):
            fn = self.eval(exp[0], env)
            args = [self.eval(arg, env) for arg in exp[1:]]
            # Global scope
            if callable(fn):
                return fn(*args)
            elif isinstance(fn, dict):
                activationRecord = {}
                for (i, param) in enumerate(fn['params']):
                    activationRecord[param] = args[i]
                activationEnvironment = Environment(activationRecord, env)
                return self.eval(fn['body'], activationEnvironment)

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
