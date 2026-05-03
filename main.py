import subprocess
import sys

def ask_qwen(query):
    result = subprocess.run(
        ["ollama", "run", "qwen3.5", query],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def stop_ollama():
    subprocess.run(["pkill", "ollama"], capture_output=True)

def main():
    print("Qwen 3.5 Chat (Ctrl+C to quit)\n")
    try:
        while True:
            query = input("You: ")
            if not query.strip():
                continue
            print("\nQwen: ")
            answer = ask_qwen(query)
            print(f"{answer}\n")
    except KeyboardInterrupt:
        print("\nGoodbye!")
        stop_ollama()
        sys.exit(0)

if __name__ == "__main__":
    main()
