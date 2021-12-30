import re

from environment import Environment
from parser import Parser
from transformer import Transformer

class Eva():
    def __init__(self, globalEnv=None):
        self.globalEnv = globalEnv
        self.parser = Parser()
        self.transformer = Transformer()

    def evaluate(self, ast):
        return self.eval(ast, self.globalEnv)

    def evalNew(self, input):
        def square(x):
            return x * x

        def sum(a, b):
            return a + b
        ast = self.parser.parse(input)
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
            # concatenation
            if self._isString(exp[1], env) and self._isString(exp[1], env):
                a = exp[1].strip('\"')
                b = exp[2].strip('\"')
                return '"' + (a + b) + '"'
            return self.eval(exp[1], env) + self.eval(exp[2], env);

        if exp[0] == '-':
            if len(exp) == 2: # unary case, (- 3)
                return -self.eval(exp[1], env)
            else:
                return self.eval(exp[1], env) - self.eval(exp[2], env)

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

        # Module (module <moduleName> <exp1> <exp2> ...)
        if exp[0] == 'module':
            # undefined number of arguments in the expression
            name = exp[1]
            moduleEnv = Environment({}, env)
            for expression in exp[2:]:
                self.eval(expression, moduleEnv)
            return env.define(name, moduleEnv)

        if exp[0] == 'prop':
            [_, instance, name] = exp
            instanceEnv = self.eval(instance, env)
            return instanceEnv.lookup(name)

        if exp[0] == 'import':
            [_, name] = exp
            f = open("modules/" + name + ".eva", 'r')
            file_contents = f.read()
            input = file_contents
            moduleName = name
            ast = self.parser.parse(input, moduleName)
            result = self.eval(ast, self.globalEnv)
            f.close()
            return moduleName


        # Functions
        if exp[0] == 'lambda':
            [_, params, body] = exp;
            return { 'params': params, 'body': body, 'env': env }

        if exp[0] == 'def':
            varExp = self.transformer.transformDefToLambda(exp)
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
