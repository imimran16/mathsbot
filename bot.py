import os
import telebot
from openai import OpenAI

# ==== ENVIRONMENT SE SECRETS LO (GitHub me hardcode mat karna) ====
TOKEN = os.getenv("TELEGRAM_TOKEN")        # Render Environment me set karo
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ==== CLIENTS BANAAO (PEHLE!) ====
bot = telebot.TeleBot(TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# ==== CHATGPT-STYLE REPLY FUNCTION ====
def ai_reply(user_text: str) -> str:
    prompt = (
        "You are ChatGPT, a friendly tutor and assistant. "
        "User jis language me baat kare, usi language me reply do. "
        "Explain clearly and simply.\n\n"
        f"User: {user_text}\n"
        "ChatGPT:"
    )

    resp = client.responses.create(
        model="gpt-4.1-mini",   # ya gpt-4o-mini agar tum use kar rahe ho
        input=prompt,
    )

    return resp.output[0].content[0].text

# ==== /start COMMAND ====
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        "🤖 Maths Genius Bot online hai!\n\n"
        "Main kya kar sakta hoon:\n"
        "• ChatGPT-style baat\n"
        "• Class 6–12 ke maths/physics doubts solve\n"
        "Bas apna sawal text me bhejo."
    )

# ==== NORMAL TEXT MESSAGES ====
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        answer = ai_reply(message.text)
        bot.reply_to(message, answer)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# ==== MAIN ENTRYPOINT (Render ke liye bhi zaroori) ====
if __name__ == "__main__":
    print("BOT RUNNING...")
    bot.infinity_polling()

