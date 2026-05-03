import subprocess
import sys

def ask_qwen(sender, message):
    prompt = f"""You are a secretary analyzing incoming messages. Analyze the following message and answer exactly these 4 questions:

1. Is this message related to the user?
2. Does this message require some action taken by the user?
3. Does the message contain any due dates or other critical things to consider?
4. What is the importance of the message (high/medium/low)?

Sender: {sender}
Message: {message}

Provide a concise analysis answering each question."""

    result = subprocess.run(
        ["ollama", "run", "qwen3.5", prompt],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def stop_ollama():
    subprocess.run(["pkill", "ollama"], capture_output=True)

def main():
    print("Qwen 3.5 Secretary (Ctrl+C to quit)\n")
    try:
        while True:
            sender = input("Sender: ")
            if not sender.strip():
                continue
            message = input("Message: ")
            if not message.strip():
                continue

            print("\nAnalyzing...\n")
            analysis = ask_qwen(sender, message)
            print(f"{analysis}\n")
    except KeyboardInterrupt:
        print("\nGoodbye!")
        stop_ollama()
        sys.exit(0)

if __name__ == "__main__":
    main()
