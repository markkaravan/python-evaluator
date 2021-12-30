class Parser():
    def __init__(self):
        pass

    def parse(self, input, moduleName=None):
        wrapper = None
        if moduleName is not None:
            wrapper = '(module ' + moduleName + ' ' + input + ')'
        else:
            wrapper = '(begin ' + input + ')'
        spaced = wrapper.replace('(', ' ( ').replace(')', ' ) ').replace('\n', ' \n ')
        tokens = self.tokenize(spaced)
        ast = self.generateAst(tokens)
        return ast

    def tokenize(self, input):
        tokens = []
        parseModes = ["Empty", "String", "QuoteString"]
        parseMode = "Empty"
        token = ""
        for c in input:
            if parseMode == "Empty":
                if c == '(':
                    tokens.append("(")
                elif c == ')':
                    tokens.append(")")
                elif c in ['', ' ', '\n']:
                    continue
                elif c == '"':
                    token = '"'
                    parseMode = "QuoteString"
                else:
                    token = ''
                    token += c
                    parseMode = "String"
            elif parseMode == "String":
                if c in ['', ' ', '\n']:
                    tokens.append(token)
                    token = ""
                    parseMode = "Empty"
                else:
                    token += c
            elif parseMode == "QuoteString":
                if c == '"':
                    token += c
                    tokens.append(token)
                    token = ""
                    parseMode = "Empty"
                else:
                    token += c
        return tokens

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
        ast = stack[0]
        return ast


# p = Parser()
# exp = """
#     (+ "Lorem ipsum " "Dolor est")
# """
# res = p.parse(exp)
# print(res)
