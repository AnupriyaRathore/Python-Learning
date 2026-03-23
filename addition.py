def add(a, b):
    """Simple function to add two numbers."""
    return a + b

# Demo usage
if __name__ == "__main__":
    num1 = 5
    num2 = 3
    result = add(num1, num2)
    print(f"{num1} + {num2} = {result}")

    # Interactive example
    x = float(input("Enter first number: "))
    y = float(input("Enter second number: "))
    print(f"{x} + {y} = {add(x, y)}")

