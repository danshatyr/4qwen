def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():
    try:
        print("Simple Addition")
        num1 = get_number("Enter first number: ")
        num2 = get_number("Enter second number: ")
        print(f"Sum: {num1 + num2}")
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
