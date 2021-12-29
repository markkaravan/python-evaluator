class Parser():
    def __init__(self):
        pass

    def parse(self, input):
        tokens = self.tokenize(input)
        ast = self.generateAst(tokens)
        return ast

    def tokenize(self, s):
        tokens = s.replace('(', ' ( ').replace(')', ' ) ').split(' ')
        cleaned = [t for t in tokens if t != '']
        return cleaned

    def generateAst(self, tokens):
        stack = []
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                branch = []
                while stack[-1] != '(':
                    branch.insert(0, stack.pop())
                stack.pop() # final '('
                stack.append(branch)
            elif token.isnumeric():
                stack.append(float(token))
            elif type(token) == str and token[0] == '"' and token[-1] == '"':
                stack.append(token)
            elif type(token) == str:
                stack.append(token)
        return stack[0]


# p = Parser()
# expressions = [
#     '(   "hello"      )',
#     '42',
#     '(+ 2 3)',
#     '(var foo (+ 2 (* 3 4)))',
# ]
#
# for exp in expressions:
#     print(p.parse(exp))
