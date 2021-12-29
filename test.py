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

    (
        """
        (= 1 1)
        """,
        True
    ),

    (
        """
        (<> 1 1)
        """,
        False
    ),

    (
        """
        (<= 1 1)
        """,
        True
    ),

    (
        """
        (>= 1 1)
        """,
        True
    ),

    (
        """
        (< 1 1)
        """,
        False
    ),

    (
        """
        (> 1 1)
        """,
        False
    ),

    (
        """
        (< 1 2)
        """,
        True
    ),

    (
        """
        (> 2 1)
        """,
        True
    ),

    (
        """
        (and (= 1 1) (<> 1 2))
        """,
        True
    ),

    (
        """
        (or (= 1 1) (<> 1 1))
        """,
        True
    ),

    (
        """
        (not (= 1 1))
        """,
        False
    ),

    (
        """
        (if
            (= 1 1)
            "One"
            "None"
        )
        """,
        '"One"'
    ),

    (
        """
        (if
            (<> 1 1)
            "One"
            "None"
        )
        """,
        '"None"'
    ),

    (
        """
        (var foo 1)
        (set foo 2)
        """,
        2
    ),

    (
        """
        (var foo 1)
        (set foo 2)
        foo
        """,
        2
    ),

    (
        """
        (var foo 1)
        (begin
            (set foo 2)
        )
        foo
        """,
        2
    ),

    (
        """
        (var foo 1)
        (begin
            (set foo 2)
            foo
        )
        """,
        2
    ),

    (
        """
        (var foo 1)
        (begin
            (begin
                (set foo 2)
            )
        )
        foo
        """,
        2
    ),

    (
        """
        (var counter 10)
        (> counter 0)
        """,
        True
    ),

    (
        """
        (var counter 10)
        (var total 0)
        (while
            (> counter 0)
            (begin
                (set total (+ total 1))
                (set counter (- counter 1))
            )
        )
        total
        """,
        10
    ),
]



globalEnv = Environment({
    'version': 1.0,
}, None);

parser = Parser()

for (actual, expected) in expressions:
    ast = parser.parse(actual)
    value = eva.eval(ast, globalEnv)
    if value == expected:
        continue
    else:
        print("fail")
        print("Actual: ", actual)
        print("Value: ", value)
        print("Expected: ", expected)
        break
else:
    print("All tests passed!")
