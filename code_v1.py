import sys

def subtract_numbers(num1: float, num2: float) -> float:
    """
    Subtracts the second number from the first number.

    Args:
        num1: The first number (minuend).
        num2: The second number (subtrahend).

    Returns:
        The result of the subtraction (difference).
    """
    return num1 - num2

def main():
    """
    Main function to get input from the user and display the subtraction result.
    Handles potential input errors gracefully.
    """
    print("-----------------------------------")
    print("   Number Subtraction Program      ")
    print("-----------------------------------")

    try:
        # Get the first number from the user
        input_str1 = input("Enter the first number: ")
        number1 = float(input_str1)

        # Get the second number from the user
        input_str2 = input("Enter the second number: ")
        number2 = float(input_str2)

        # Perform the subtraction
        result = subtract_numbers(number1, number2)

        # Display the result
        print(f"\n{number1} - {number2} = {result}")
        print("-----------------------------------")

    except ValueError:
        print("\nError: Invalid input. Please enter valid numbers.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()