import json
import csv
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)



def loading_messages(filepath):
    with open (filepath, 'r', encoding="utf-8") as file:
        messages = json.load(file)
    return messages

def cleaned_messages(messages):
    seen = set()
    cleaned = []
    for message in messages:
        if not message.get("user_id"):
           logger.warning(f"Skipped wrong user_id, message'{message.get('message', '')[:30]}'")
           continue

        if not message.get("message") or not message["message"].strip():
           logger.warning(f"Skipped empty message, message'{message.get('user_id')}")
           continue

        if not message.get("channel"):
            logger.warning(f"Skipped: missing channel, user_id={message.get('user_id')}")
            continue

        key = (message.get("user_id"), message.get("message"), message.get("created_at"))

        if key in seen:
            logger.warning(f"Skipped: duplicate message, user_id={message.get('user_id')}")
            continue

        seen.add(key)

        message["message"] = message["message"].strip()
        cleaned.append(message)

    logger.info(f'Cleaned: {len(cleaned)} from {len(messages)} ')
    return cleaned
    

def classify_messages(text):
    text_lowered = text.lower()

    if any(word in text_lowered for word in ['grant', 'funding', 'deadline', 'scholarship']):
        return 'grant_search'
    if any(word in text_lowered for word in ['report', 'file', 'send again', 'document']):
        return 'report_request'
    if any(word in text_lowered for word in ['how', 'what', 'can you', 'where', 'why']):
        return 'general_question'
    return 'unknown'

def save_in_database():
    pass

def save_csv(messages, filepath):
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['user_id', 'message', 'created_at', 'channel', 'category'])
        writer.writeheader()
        writer.writerows(messages)
    
    logger.info(f"Saved CSV to {filepath}")


def save_report(messages, filepath):
    categories = {}
    channels = {}
    users = {}

    for message in messages:
        category = message["category"]
        categories[category] = categories.get(category, 0) + 1

        channel = message["channel"]
        channels[channel] = channels.get(channel, 0) + 1

        user = message["user_id"]
        users[user] = users.get(user, 0) + 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Total messages: {len(messages)}\n")
        f.write(f"Total categories: {len(categories)}\n")
        f.write(f"Total channels: {len(channels)}\n")
        f.write(f"Total users: {len(users)}\n")
    
        f.write(f"Categories:")
        for category, count in categories.items():
            f.write(f"  {category}: {count}\n")
    
        f.write(f"Channels:")
        for channel, count in channels.items():
            f.write(f"  {channel}: {count}\n")
    
        f.write(f"Users:")
        for user, count in users.items():
            f.write(f"  {user}: {count}\n")

    logger.info(f"Saved report to {filepath}")

def main():
    messages = loading_messages("data/messages.json")
    logger.info(f"Loaded {len(messages)} messages")
    cleaned = cleaned_messages(messages)
    for message in cleaned:
        message['category'] = classify_messages(message['message'])
        logger.info(f"user_id={message['user_id']} → {message['category']}")
    save_csv(cleaned, "output/classified_messages.csv")
    save_report(cleaned, "output/summary_report.txt")
    
if __name__ == "__main__":
    main()