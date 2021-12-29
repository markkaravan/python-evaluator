class Parser():
    def __init__(self):
        print("Initializing parser")

    def parse(self, input):
        tokens = self.tokenize(input)
        # ast = self.generateAst(tokens, [])
        return tokens

    def tokenize(self, s):
        tokens = s.replace('(', ' ( ').replace(')', ' ) ').split(' ')
        cleaned = [t for t in tokens if t != '']
        return cleaned

    # def generateAst(self, tokens, ast):
    #     for token in tokens:





p = Parser()
expressions = [
    '(   "hello"      )',
    '42',
    '(+ 2 3)',
    '(var foo (+ 2 (* 3 4)))',
]

for exp in expressions:
    print(p.parse(exp))
