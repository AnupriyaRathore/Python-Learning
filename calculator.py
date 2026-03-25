#!/usr/bin/env python3
"""Simple interactive calculator program."""

def get_number(prompt):
    while True:
        try:
            value = input(prompt).strip()
            return float(value)
        except ValueError:
            print("Invalid number. Please enter a valid numeric value.")


def choose_operator():
    ops = {
        "1": ("+", "Addition"),
        "2": ("-", "Subtraction"),
        "3": ("*", "Multiplication"),
        "4": ("/", "Division"),
        "5": ("%", "Modulus"),
        "6": ("**", "Power"),
        "7": ("//", "Floor division")
    }

    print("\nChoose operation:")
    for key, (symbol, label) in ops.items():
        print(f" {key}. {label} ({symbol})")

    while True:
        choice = input("Enter choice [1-7] or q to quit: ").strip().lower()
        if choice == "q":
            return None
        if choice in ops:
            return ops[choice][0]
        print("Invalid selection. Please choose a valid option.")


def calculate(a, op, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
    if op == "%":
        if b == 0:
            raise ZeroDivisionError("Cannot modulus by zero")
        return a % b
    if op == "**":
        return a ** b
    if op == "//":
        if b == 0:
            raise ZeroDivisionError("Cannot floor-divide by zero")
        return a // b
    raise ValueError(f"Unsupported operation '{op}'")


def main():
    print("Simple Calculator")
    print("Type 'q' at any input prompt to quit")

    while True:
        op = choose_operator()
        if op is None:
            print("Exiting calculator. Goodbye!")
            break

        try:
            num1 = get_number("Enter first number: ")
            num2 = get_number("Enter second number: ")
            result = calculate(num1, op, num2)
            print(f"Result: {num1} {op} {num2} = {result}")
        except ZeroDivisionError as e:
            print("Error:", e)
        except Exception as e:
            print("Unexpected error:", e)

        print("\n---")


if __name__ == "__main__":
    main()
