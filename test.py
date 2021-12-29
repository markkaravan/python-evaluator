from eva import Eva
from environment import Environment
from parser import Parser

eva = Eva();

expressions = [
    (
        """
        "Foo"
        """,
        '"Foo"'
    ),

    (
        """
        35
        """,
        35
    ),

    (
        """
        (+ 1 2)
        """,
        3
    ),


    (
        """
        (* 2 3)
        """,
        6
    ),

    (
        """
        (+ (* 3 3) (* 4 4))
        """,
        25
    ),

    (
        """
        (var x 10)
        """,
        10
    ),

    (
        """
        version
        """,
        1.0
    ),

    (
        """
        (begin
            (+ 2 2)
        )
        """,
        4.0
    ),
    (
        """
        (begin
            (+ 2 2)
            (+ 2 3)
            (+ 2 4)
        )
        """,
        6.0
    ),
    (
        """
        (begin
            (var version 2)
            version
        )
        """,
        2.0
    ),
    (
        """
        (begin
            (var version 2)
            (begin
                (var version 3)
                version
            )
        )
        """,
        3.0
    ),
    (
        """
        (begin
            (var version 2)
            (begin
                (var version 3)
            )
            version
        )
        """,
        2.0
    ),
    (
        """
        (begin
            (var version 2)
            (begin
                version
            )
        )
        """,
        2.0
    ),
    (
        """
        (+ 1 2)
        (+ 3 4)
        """,
        7.0
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
