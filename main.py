import json
import subprocess
import sys
import urllib.request

API_URL = "http://127.0.0.1:11434/api/generate"

def ask_qwen(sender, message):
    prompt = f"""You are a secretary analyzing incoming messages. Analyze the following message and answer exactly these 4 questions:

1. Is this message related to the user?
2. Does this message require some action taken by the user?
3. Does the message contain any due dates or other critical things to consider?
4. What is the importance of the message (high/medium/low)?

Sender: {sender}
Message: {message}

Provide a concise analysis answering each question."""

    payload = json.dumps({
        "model": "qwen3.5",
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))["response"].strip()

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
            print(ask_qwen(sender, message), "\n")
    except KeyboardInterrupt:
        print("\nGoodbye!")
        stop_ollama()
        sys.exit(0)

if __name__ == "__main__":
    main()
