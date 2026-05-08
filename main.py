import asyncio
import json
import subprocess
import urllib.request
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import ChannelPrivateError, FloodWaitError

API_URL = "http://127.0.0.1:11434/api/generate"
CHECK_INTERVAL = 3600
PROCESSED_FILE = "processed_messages.json"


def load_processed():
    try:
        with open(PROCESSED_FILE, "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()


def save_processed(processed):
    with open(PROCESSED_FILE, "w") as f:
        json.dump(list(processed), f)


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

    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            return json.loads(response.read().decode("utf-8")).get("response", "").strip()
    except Exception as e:
        return f"Error calling Qwen: {e}"


async def ask_qwen_async(sender, message):
    return await asyncio.get_event_loop().run_in_executor(None, ask_qwen, sender, message)


def stop_ollama():
    subprocess.run(["pkill", "ollama"], capture_output=True)


async def analyze_messages(client, channel_name, processed):
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking {channel_name}...")

    try:
        messages = await client.get_messages(channel_name, limit=50)
    except (ChannelPrivateError, ValueError) as e:
        print(f"Error accessing channel: {e}")
        return

    new_count = 0
    for msg in messages:
        if not msg.text or msg.id in processed:
            continue

        new_count += 1
        sender = "Unknown"
        if msg.sender:
            sender = msg.sender.username or msg.sender.first_name or str(msg.sender_id)

        print(f"\n--- Message {msg.id} from {sender} ---")
        print(f"Text: {msg.text[:200]}...")

        print("\nAnalysis:")
        print(await ask_qwen_async(sender, msg.text))

        processed.add(msg.id)

    if new_count == 0:
        print("No new messages.")
    else:
        print(f"\nProcessed {new_count} new message(s).")
        save_processed(processed)


async def main():
    print("Qwen 3.5 Secretary - Telegram Monitor\n")

    try:
        api_id = input("Enter your Telegram API ID: ").strip()
        api_hash = input("Enter your Telegram API Hash: ").strip()
        channel = input("Enter channel name/username: ").strip()
    except EOFError:
        return

    if not all([api_id, api_hash, channel]):
        print("All fields are required.")
        return

    client = TelegramClient("session", int(api_id), api_hash)
    try:
        await client.start()
    except Exception as e:
        print(f"Failed to connect to Telegram: {e}")
        return

    processed = load_processed()
    print(f"\nMonitoring {channel} every hour. Press Ctrl+C to stop.\n")

    try:
        while True:
            await analyze_messages(client, channel, processed)
            print(f"\nWaiting {CHECK_INTERVAL // 60} minutes until next check...")
            await asyncio.sleep(CHECK_INTERVAL)
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\nGoodbye!")
    finally:
        await client.disconnect()
        stop_ollama()


if __name__ == "__main__":
    asyncio.run(main())
