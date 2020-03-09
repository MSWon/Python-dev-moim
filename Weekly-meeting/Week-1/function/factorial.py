def factorial(n):
    "return n!"
    return 1 if n < 2 else n * factorial(n-1)

if __name__ == "__main__":
    factorial(4)
    factorial.__doc__
    type(factorial)

    fact = factorial

    fact(5)
    list(map(fact, range(11)))