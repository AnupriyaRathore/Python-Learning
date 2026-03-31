"""
Comprehensive Addition Program Demonstrating All OOP Concepts in Python

This program showcases:
1. Classes and Objects
2. Inheritance (Single, Multiple, Multilevel)
3. Polymorphism (Method Overriding, Duck Typing)
4. Encapsulation (Private Attributes, Properties)
5. Abstraction (Abstract Base Classes)
6. Class Methods and Static Methods
7. Dunder Methods (Operator Overloading)
8. Composition and Aggregation
9. Mixins
10. Exception Handling
"""

from abc import ABC, abstractmethod
from typing import List, Union, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ===============================
# 1. ABSTRACTION - Abstract Base Class
# ===============================
class AbstractAdder(ABC):
    """Abstract base class for all addition operations."""

    @abstractmethod
    def add(self, *args) -> Union[int, float, complex]:
        """Abstract method for addition."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Abstract method to get description of the adder."""
        pass

# ===============================
# 2. ENCAPSULATION - Private Attributes and Properties
# ===============================
class NumberValidator:
    """Helper class for number validation with encapsulation."""

    def __init__(self):
        self._allowed_types = (int, float, complex)

    def _validate_number(self, num) -> bool:
        """Private method to validate if input is a number."""
        return isinstance(num, self._allowed_types)

    def validate_and_convert(self, num) -> Union[int, float, complex]:
        """Public method to validate and convert input to number."""
        if not self._validate_number(num):
            try:
                return float(num)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid number: {num}")
        return num

# ===============================
# 3. COMPOSITION - History Logger
# ===============================
class OperationHistory:
    """Class to maintain history of operations using composition."""

    def __init__(self):
        self._history: List[dict] = []

    def add_record(self, operation: str, inputs: tuple, result, timestamp: Optional[datetime] = None):
        """Add a record to history."""
        if timestamp is None:
            timestamp = datetime.now()
        self._history.append({
            'operation': operation,
            'inputs': inputs,
            'result': result,
            'timestamp': timestamp
        })

    def get_history(self) -> List[dict]:
        """Get all history records."""
        return self._history.copy()

    def clear_history(self):
        """Clear all history."""
        self._history.clear()

    def get_last_operation(self) -> Optional[dict]:
        """Get the last operation performed."""
        return self._history[-1] if self._history else None

# ===============================
# 4. MIXINS - Additional Functionality
# ===============================
class LoggingMixin:
    """Mixin class for logging functionality."""

    def log_operation(self, message: str):
        """Log an operation."""
        logging.info(f"{self.__class__.__name__}: {message}")

class PrecisionMixin:
    """Mixin for precision handling."""

    def __init__(self, precision: int = 2):
        self._precision = precision

    @property
    def precision(self) -> int:
        return self._precision

    @precision.setter
    def precision(self, value: int):
        if value < 0:
            raise ValueError("Precision must be non-negative")
        self._precision = value

    def round_result(self, result: float) -> float:
        """Round result to specified precision."""
        return round(result, self._precision)

# ===============================
# 5. BASIC ADDER CLASS - Foundation
# ===============================
class BasicAdder(AbstractAdder, LoggingMixin, PrecisionMixin):
    """Basic addition class implementing AbstractAdder with mixins."""

    def __init__(self, precision: int = 2):
        PrecisionMixin.__init__(self, precision)
        self._validator = NumberValidator()  # Composition
        self._history = OperationHistory()   # Composition
        self._operation_count = 0

    def add(self, *args) -> Union[int, float, complex]:
        """Add multiple numbers."""
        if not args:
            return 0

        # Validate and convert all inputs
        validated_args = []
        for arg in args:
            validated_args.append(self._validator.validate_and_convert(arg))

        # Perform addition
        result = sum(validated_args)

        # Apply precision if result is float
        if isinstance(result, float):
            result = self.round_result(result)

        # Log and record operation
        self._operation_count += 1
        operation_desc = f"Added {len(args)} numbers"
        self.log_operation(operation_desc)
        self._history.add_record('addition', args, result)

        return result

    def get_description(self) -> str:
        """Get description of this adder."""
        return f"Basic Adder with {self.precision} decimal precision"

    @property
    def operation_count(self) -> int:
        """Property to get operation count."""
        return self._operation_count

    @classmethod
    def create_with_precision(cls, precision: int) -> 'BasicAdder':
        """Class method to create adder with specific precision."""
        return cls(precision)

    @staticmethod
    def is_number(value) -> bool:
        """Static method to check if value is a number."""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

# ===============================
# 6. INHERITANCE - Single Inheritance
# ===============================
class AdvancedAdder(BasicAdder):
    """Advanced adder with additional features."""

    def __init__(self, precision: int = 2, memory: bool = True):
        super().__init__(precision)
        self._memory = 0.0 if memory else None
        self._memory_enabled = memory

    def add_to_memory(self, value):
        """Add value to memory."""
        if self._memory_enabled:
            validated_value = self._validator.validate_and_convert(value)
            self._memory += validated_value
            self.log_operation(f"Added {value} to memory. New memory: {self._memory}")

    def get_memory(self) -> Optional[float]:
        """Get current memory value."""
        return self._memory

    def clear_memory(self):
        """Clear memory."""
        if self._memory_enabled:
            self._memory = 0.0
            self.log_operation("Memory cleared")

    def add_with_memory(self, *args) -> Union[int, float, complex]:
        """Add numbers and include memory value."""
        result = self.add(*args)
        if self._memory_enabled and self._memory != 0:
            result += self._memory
            self.log_operation(f"Added memory ({self._memory}) to result")
        return result

# ===============================
# 7. POLYMORPHISM - Method Overriding
# ===============================
class ScientificAdder(AdvancedAdder):
    """Scientific adder with special number handling."""

    def add(self, *args) -> Union[int, float, complex]:
        """Override add method with scientific notation support."""
        # Handle scientific notation strings
        processed_args = []
        for arg in args:
            if isinstance(arg, str) and ('e' in arg.lower() or 'E' in arg):
                try:
                    # Convert scientific notation
                    processed_args.append(float(arg))
                except ValueError:
                    processed_args.append(self._validator.validate_and_convert(arg))
            else:
                processed_args.append(self._validator.validate_and_convert(arg))

        # Call parent add method
        result = super().add(*processed_args)

        # Additional scientific formatting
        if isinstance(result, float) and abs(result) >= 1000:
            self.log_operation(f"Large result: {result:.2e}")

        return result

    def get_description(self) -> str:
        """Override description."""
        return f"Scientific Adder with memory support and {self.precision} decimal precision"

# ===============================
# 8. MULTIPLE INHERITANCE
# ===============================
class StatisticalMixin:
    """Mixin for statistical operations."""

    def __init__(self):
        self._stats_history = []

    def calculate_average(self, numbers: List[Union[int, float]]) -> float:
        """Calculate average of numbers."""
        if not numbers:
            return 0.0
        return sum(numbers) / len(numbers)

    def calculate_median(self, numbers: List[Union[int, float]]) -> float:
        """Calculate median of numbers."""
        if not numbers:
            return 0.0
        sorted_nums = sorted(numbers)
        n = len(sorted_nums)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
        return sorted_nums[mid]

class StatisticalAdder(BasicAdder, StatisticalMixin):
    """Adder with statistical capabilities using multiple inheritance."""

    def __init__(self, precision: int = 2):
        BasicAdder.__init__(self, precision)
        StatisticalMixin.__init__(self)

    def add_with_stats(self, *args) -> dict:
        """Add numbers and return statistical information."""
        validated_args = [self._validator.validate_and_convert(arg) for arg in args]
        result = self.add(*args)

        stats = {
            'sum': result,
            'count': len(validated_args),
            'average': self.calculate_average(validated_args),
            'median': self.calculate_median(validated_args),
            'min': min(validated_args) if validated_args else 0,
            'max': max(validated_args) if validated_args else 0
        }

        self._stats_history.append(stats)
        self.log_operation(f"Calculated statistics for {len(args)} numbers")

        return stats

# ===============================
# 9. OPERATOR OVERLOADING - Dunder Methods
# ===============================
class NumberCollection:
    """Class representing a collection of numbers with operator overloading."""

    def __init__(self, *numbers):
        self._validator = NumberValidator()
        self._numbers = [self._validator.validate_and_convert(n) for n in numbers]
        self._history = OperationHistory()

    def __add__(self, other):
        """Overload + operator for collection addition."""
        if isinstance(other, NumberCollection):
            # Add corresponding elements
            min_len = min(len(self._numbers), len(other._numbers))
            result_nums = [self._numbers[i] + other._numbers[i] for i in range(min_len)]

            # Add remaining elements from longer collection
            if len(self._numbers) > len(other._numbers):
                result_nums.extend(self._numbers[min_len:])
            elif len(other._numbers) > len(self._numbers):
                result_nums.extend(other._numbers[min_len:])

            result = NumberCollection(*result_nums)
            result._history.add_record('collection_addition', (self._numbers, other._numbers), result._numbers)
            return result

        elif isinstance(other, (int, float, complex)):
            # Add scalar to all elements
            result_nums = [n + other for n in self._numbers]
            result = NumberCollection(*result_nums)
            result._history.add_record('scalar_addition', (self._numbers, other), result._numbers)
            return result

        return NotImplemented

    def __str__(self):
        """String representation."""
        return f"NumberCollection({self._numbers})"

    def __repr__(self):
        """Detailed string representation."""
        return f"NumberCollection(*{self._numbers})"

    def __len__(self):
        """Length of collection."""
        return len(self._numbers)

    def __getitem__(self, index):
        """Get item by index."""
        return self._numbers[index]

    def __iter__(self):
        """Make collection iterable."""
        return iter(self._numbers)

    def sum(self) -> Union[int, float, complex]:
        """Sum all numbers in collection."""
        return sum(self._numbers)

# ===============================
# 10. AGGREGATION - Calculator Class
# ===============================
class Calculator:
    """Calculator class demonstrating aggregation of different adders."""

    def __init__(self):
        self._adders = {
            'basic': BasicAdder(),
            'advanced': AdvancedAdder(),
            'scientific': ScientificAdder(),
            'statistical': StatisticalAdder()
        }
        self._current_adder = self._adders['basic']
        self._global_history = OperationHistory()

    def set_adder_type(self, adder_type: str):
        """Set the current adder type."""
        if adder_type in self._adders:
            self._current_adder = self._adders[adder_type]
            logging.info(f"Switched to {adder_type} adder")
        else:
            raise ValueError(f"Unknown adder type: {adder_type}")

    def add(self, *args) -> Union[int, float, complex, dict]:
        """Perform addition using current adder."""
        result = self._current_adder.add(*args)
        self._global_history.add_record(
            f"{self._current_adder.__class__.__name__}_addition",
            args, result
        )
        return result

    def get_available_adders(self) -> List[str]:
        """Get list of available adder types."""
        return list(self._adders.keys())

    def get_global_history(self) -> List[dict]:
        """Get global operation history."""
        return self._global_history.get_history()

# ===============================
# 11. EXCEPTION HANDLING
# ===============================
class AdditionError(Exception):
    """Custom exception for addition operations."""
    pass

class AdditionProgram:
    """Main program class with comprehensive error handling."""

    def __init__(self):
        self.calculator = Calculator()

    def safe_add(self, *args):
        """Safely perform addition with comprehensive error handling."""
        try:
            # Validate inputs
            if not args:
                raise AdditionError("At least one number is required for addition")

            # Check for None values
            if any(arg is None for arg in args):
                raise AdditionError("None values are not allowed")

            # Attempt addition
            result = self.calculator.add(*args)
            return result

        except ValueError as e:
            logging.error(f"Value error during addition: {e}")
            raise AdditionError(f"Invalid input: {e}")
        except TypeError as e:
            logging.error(f"Type error during addition: {e}")
            raise AdditionError(f"Type mismatch: {e}")
        except OverflowError as e:
            logging.error(f"Overflow error during addition: {e}")
            raise AdditionError("Result too large to handle")
        except Exception as e:
            logging.error(f"Unexpected error during addition: {e}")
            raise AdditionError(f"Unexpected error: {e}")

    def demonstrate_oop_concepts(self):
        """Demonstrate all OOP concepts implemented in this program."""
        print("=" * 60)
        print("COMPREHENSIVE ADDITION PROGRAM - OOP CONCEPTS DEMONSTRATION")
        print("=" * 60)

        # 1. Classes and Objects
        print("\n1. CLASSES AND OBJECTS:")
        basic_adder = BasicAdder()
        result = basic_adder.add(5, 3)
        print(f"BasicAdder object: {result}")

        # 2. Inheritance
        print("\n2. INHERITANCE:")
        advanced_adder = AdvancedAdder()
        advanced_adder.add_to_memory(10)
        result = advanced_adder.add_with_memory(5, 3)
        print(f"AdvancedAdder with memory: {result}")

        # 3. Polymorphism
        print("\n3. POLYMORPHISM (Method Overriding):")
        scientific_adder = ScientificAdder()
        result1 = scientific_adder.add(1.5e3, 2.5e2)  # Scientific notation
        result2 = basic_adder.add(1.5e3, 2.5e2)       # Regular
        print(f"Scientific: {result1}, Basic: {result2}")

        # 4. Encapsulation
        print("\n4. ENCAPSULATION (Properties):")
        print(f"BasicAdder precision: {basic_adder.precision}")
        basic_adder.precision = 4
        print(f"After setting precision: {basic_adder.precision}")

        # 5. Abstraction
        print("\n5. ABSTRACTION (Abstract Base Class):")
        print(f"BasicAdder description: {basic_adder.get_description()}")

        # 6. Class and Static Methods
        print("\n6. CLASS AND STATIC METHODS:")
        adder_from_class = BasicAdder.create_with_precision(3)
        print(f"Created with class method, precision: {adder_from_class.precision}")
        print(f"Is '123' a number? {BasicAdder.is_number('123')}")
        print(f"Is 'abc' a number? {BasicAdder.is_number('abc')}")

        # 7. Operator Overloading
        print("\n7. OPERATOR OVERLOADING:")
        collection1 = NumberCollection(1, 2, 3)
        collection2 = NumberCollection(4, 5, 6)
        result_collection = collection1 + collection2
        print(f"Collection addition: {collection1} + {collection2} = {result_collection}")

        # 8. Composition and Aggregation
        print("\n8. COMPOSITION AND AGGREGATION:")
        calc = Calculator()
        calc.set_adder_type('statistical')
        stats = calc.add(1, 2, 3, 4, 5)
        print(f"Statistical addition result: {stats}")

        # 9. Exception Handling
        print("\n9. EXCEPTION HANDLING:")
        try:
            self.safe_add(1, "invalid")
        except AdditionError as e:
            print(f"Caught AdditionError: {e}")

        # 10. History and Logging
        print("\n10. HISTORY AND LOGGING:")
        print(f"Operations performed: {basic_adder.operation_count}")
        history = basic_adder._history.get_history()  # Accessing private attribute for demo
        print(f"History records: {len(history)}")

        print("\n" + "=" * 60)
        print("ALL OOP CONCEPTS DEMONSTRATED SUCCESSFULLY!")
        print("=" * 60)

# ===============================
# MAIN EXECUTION
# ===============================
if __name__ == "__main__":
    program = AdditionProgram()

    # Run demonstration
    program.demonstrate_oop_concepts()

    # Interactive usage
    print("\n" + "=" * 60)
    print("INTERACTIVE ADDITION PROGRAM")
    print("=" * 60)

    while True:
        try:
            print("\nAvailable adder types:", program.calculator.get_available_adders())
            adder_type = input("Choose adder type (basic/advanced/scientific/statistical) or 'quit': ").lower()

            if adder_type == 'quit':
                break

            if adder_type in program.calculator.get_available_adders():
                program.calculator.set_adder_type(adder_type)

                numbers_input = input("Enter numbers separated by spaces: ")
                numbers = []

                for num_str in numbers_input.split():
                    try:
                        numbers.append(float(num_str))
                    except ValueError:
                        print(f"Invalid number: {num_str}")
                        continue

                if numbers:
                    result = program.safe_add(*numbers)
                    print(f"Result: {result}")
                else:
                    print("No valid numbers entered.")
            else:
                print("Invalid adder type.")

        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"Interactive mode error: {e}")

