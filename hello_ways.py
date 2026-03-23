#!/usr/bin/env python3
"""
Multiple ways to print "Hello" (or "Hello, World!") in Python.
Run: python hello_ways.py
"""

print("1. Basic print():")
print("Hello, World!")

print("\n2. Print with sep/end:")
print("Hello", "World", sep=", ", end="!\n")

print("\n3. f-string (Python 3.6+):")
name = "World"
print(f"Hello, {name}!")

print("\n4. .format() (Python 2.6+):")
print("Hello, {}!".format(name))

print("\n5. % operator:")
print("Hello, %s!" % name)

print("\n6. Print multiple lines:")
print("""
7. Triple quotes multiline:
Hello!
How are you?
""")

print("\n8. From bytes:")
print(b"Hello, World!".decode())

print("\n9. Using sys.stdout.write:")
import sys
sys.stdout.write("Hello via sys.stdout.write!\n")

print("\n10. Print with file= (to stdout):")
print("Hello via file=", file=sys.stdout)

print("\n11. Unicode:")
print("👋 Hello, World! 👋")

print("\n12. From list join:")
words = ["Hello", "World"]
print(" ".join(words) + "!")

print("\n13. Lambda one-liner:")
print((lambda s: s)( "Hello, World!" ))

print("\n14. Exec:")
exec('print("Hello via exec!")')

print("\n15. From variable reassignment:")
msg = "Hello"
msg += ", World!"
print(msg)

print("\nTotal: 15+ ways (Python 3). More exist (e.g., C extensions, generators).")

