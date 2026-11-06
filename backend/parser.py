
import re
from datetime import datetime


def parse_chat(chat_text):
    """
    Parse a WhatsApp TXT export into structured messages.
    Supports common WhatsApp date and time formats.
    """

    messages = []

    pattern = re.compile(
        r"^\[?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}),?\s+"
        r"(\d{1,2}:\d{2}(?::\d{2})?\s?(?:AM|PM|am|pm)?)\]?"
        r"\s*[-–]\s*(.*?):\s(.*)$"
    )

    current_message = None

    for line in chat_text.splitlines():

        match = pattern.match(line)

        if match:
            if current_message:
                messages.append(current_message)

            date_text, time_text, sender, message = match.groups()

            timestamp = None

            for fmt in (
                "%d/%m/%y %I:%M %p",
                "%d/%m/%Y %I:%M %p",
                "%m/%d/%y %I:%M %p",
                "%m/%d/%Y %I:%M %p",
                "%d-%m-%y %H:%M",
                "%d-%m-%Y %H:%M",
                "%d/%m/%y %H:%M",
                "%d/%m/%Y %H:%M",
            ):
                try:
                    timestamp = datetime.strptime(
                        f"{date_text} {time_text.strip()}",
                        fmt
                    )
                    break
                except ValueError:
                    continue

            current_message = {
                "timestamp": timestamp,
                "sender": sender.strip(),
                "message": message.strip()
            }

        elif current_message:
            current_message["message"] += "\n" + line

    if current_message:
        messages.append(current_message)

    return messages


def get_participants(messages):
    return sorted(set(
        msg["sender"] for msg in messages
    ))


def get_chat_statistics(messages):
    return {
        "total_messages": len(messages),
        "participants": len(get_participants(messages)),
        "participant_names": get_participants(messages)
    }
