class InputError(Exception):
    """Custom exception for input-related errors."""
    pass

class OverflowError(Exception):
    """Custom exception for overflow errors."""
    pass

def validate_input(input_str):
    """Validate and parse input string into three integers."""
    try:
        numbers = list(map(int, input_str.strip().split()))
        if len(numbers) != 3:
            raise InputError("Invalid input: Exactly three numbers are required.")
        return numbers
    except ValueError:
        raise InputError("Invalid input: Non-numeric value entered.")

def add_numbers(numbers):
    """Add three numbers and handle potential overflow."""
    try:
        total = sum(numbers)
        # Check for overflow/underflow
        if total > 2**31 - 1 or total < -2**31:
            raise OverflowError("Overflow error: Sum exceeds representable value.")
        return total
    except OverflowError as e:
        raise e

def main():
    """Main function to run the three-number adder."""
    try:
        input_str = input("Enter three numbers separated by spaces: ")
        numbers = validate_input(input_str)
        result = add_numbers(numbers)
        print(f"Sum: {result}")
    except InputError as e:
        print(f"Error: {e}")
    except OverflowError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()