from eva import Eva 

eva = Eva();

expressions = [
    (
        "String",
        "String"
    ),

    (
        35,
        35
    ),

    (
        ['+', 1, 2],
        3
    ),

    (
        ['*', 2, 3],
        7
    ),

    (
        ['+', ['*', 3, 3], ['*', 4, 4]],
        25
    ),
]


for (actual, expected) in expressions:
    if eva.eval(actual) == expected:
        print("success!")
    else:
        print("fail")
        print("Actual: ", actual)
        print("Expected: ", expected)
        break
