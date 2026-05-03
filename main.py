import subprocess
import sys

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)

def ask_qwen(num1, num2):
    prompt = f"What is the sum of {num1} and {num2}?"
    result = subprocess.run(
        ["ollama", "run", "qwen3.5", prompt],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def main():
    try:
        print("Qwen 3.5 Math Assistant")
        num1 = get_number("Enter first number: ")
        num2 = get_number("Enter second number: ")
        print("\nAsking Qwen 3.5...\n")
        answer = ask_qwen(num1, num2)
        print(answer)
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
