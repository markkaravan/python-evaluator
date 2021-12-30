from eva import Eva
from environment import Environment
from parser import Parser

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

    (
        """
        (square 3)
        """,
        9
    ),

    (
        """
        (sum 1 2)
        """,
        3
    ),

    (
        """
        (sum (square 2) (square 3))
        """,
        13
    ),

    (
        """
        (var product (lambda (a b) (* a b )))
        (product 4 5)
        """,
        20
    ),

    (
        """
        ((lambda (a b) (* a b )) 3 4)
        """,
        12
    ),

    (
        """
        (def product (a b) (* a b))
        (product 5 6)
        """,
        30
    ),

    (
        """
        (def factorial (x)
            (if (= x 1)
                x
                (* x (factorial (- x 1)))
            )
        )
        (factorial 5)
        """,
        120
    ),

    (
        """
        (+ "Hello " "world")
        """,
        '"Hello world"'
    ),

    (
        """
        (- (+ 2 3))
        """,
        -5
    ),

    (
        """
    (module Math
      (def abs (value)
        (if (< value 0) (- value) value)
      )

      (def square (x)
        (* x x)
      )

      (var MAX_VALUE 1000)
     )

     ((prop Math abs) (- 10))
        """,
        10
    ),

    (
        """
        (import Math)
        """,
        'Math'
    ),

    (
        """
        (import Math)
        ((prop Math cube) 3)

        """,
        27
    ),

    (
        """
        (var foo (cons 1 2))
        (car foo)
        """,
        1
    ),

    (
        """
        (var foo (cons 1 2))
        (cdr foo)
        """,
        2
    ),

    (
        """
        (var list (cons 1 (cons 2 (cons 3 (cons 4 nil)))))
        (car list)
        """,
        1
    ),

    (
        """
        (var list (cons 1 (cons 2 (cons 3 (cons 4 nil)))))
        (car (cdr (cdr list)))
        """,
        3
    ),


    (
        """
        (var list (cons 1 (cons 2 (cons 3 (cons 4 nil)))))
        (car (cdr (cdr list)))
        """,
        3
    ),

    (
        """
        (def build-range (start end)
            (if (> start end)
                nil
                (cons start (build-range (+ start 1) end))
            )
        )
        (var my-list (build-range 1 5))
        (car my-list)

        """,
        1
    ),

    (
        """
        (import Math)
        (def build-range (start end)
            (if (> start end)
                nil
                (cons start (build-range ((prop Math inc) start) end))
            )
        )
        (var my-list (build-range 1 5))
        (car my-list)

        """,
        1
    ),

    (
        """
        (def build-range (start end)
            (if (> start end)
                nil
                (cons start (build-range ((prop Math inc) start) end))
            )
        )
        (var my-list (build-range 10 20))

        (def get-nth (n list)
            (if (= n 0)
                (car list)
                (get-nth (- n 1) (cdr list))
            )
        )

        (get-nth 5 my-list)
        """,
        15
    ),

    (
        """
        (def build-range (start end)
            (if (> start end)
                nil
                (cons start (build-range ((prop Math inc) start) end))
            )
        )
        (var my-list (build-range 1 20))

        (def length-inner (list index)
            (if (= (cdr list) nil)
                index
                (length-inner (cdr list) (+ index 1))
            )
        )

        (length-inner my-list 1)
        """,
        20
    ),

    (
        """
        (def build-range (start end)
            (if (> start end)
                nil
                (cons start (build-range ((prop Math inc) start) end))
            )
        )
        (var my-list (build-range 1 20))

        (def length-inner (list index)
            (if (= (cdr list) nil)
                index
                (length-inner (cdr list) (+ index 1))
            )
        )

        (def length (list) (length-inner list 1))

        (length my-list)
        """,
        20
    ),

    (
        """
        (def build-range (start end)
            (if (> start end)
                nil
                (cons start (build-range ((prop Math inc) start) end))
            )
        )
        (var my-list (build-range 1 20))

        (def length (list)
            (begin
                (def length-inner (list index)
                    (if (= (cdr list) nil)
                        index
                        (length-inner (cdr list) (+ index 1))
                    )
                )
                (length-inner list 1)
            )
        )

        (length my-list)
        """,
        20
    ),


]

parser = Parser()

for (actual, expected) in expressions:
    ast = parser.parse(actual)
    eva = Eva();
    value = eva.evaluate(ast)
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
