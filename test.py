from eva import Eva
from environment import Environment
from parser import Parser

eva = Eva();

expressions = [
    (
        '"Foo"',
        '"Foo"'
    ),

    (
        '35',
        35
    ),

    (
        '(+ 1 2)',
        3
    ),


    (
        '(* 2 3)',
        6
    ),

    (
        '(+ (* 3 3) (* 4 4))',
        25
    ),

    (
        '(var x 10)',
        10
    ),

    (
        'version',
        1.0
    ),
]



globalEnv = Environment({
    'version': 1.0,
}, None);

parser = Parser()

for (actual, expected) in expressions:
    ast = parser.parse(actual)
    if eva.eval(ast, globalEnv) == expected:
        continue
    else:
        print("fail")
        print("Actual: ", actual)
        print("Expected: ", expected)
        break
else:
    print("All tests passed!")
