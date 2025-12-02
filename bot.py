import telebot
from openai import OpenAI
import os
import base64
# -----------------------------------
# /start COMMAND — ChatGPT Style Intro
# -----------------------------------
@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(
        message,
        "🤖 *Hello! I am Maths Genius AI Bot — just like genius!*\n\n"
        "📌 Main kya kar sakta hoon?\n"
        "•  natural conversation\n"
        "• Class 6–12 ke maths/physics/chemistry questions solve\n"
        "• Photo se question solve (AI Vision)\n"
        "• hum dono gupsup bhi kar sakte hai\n"
        "• Simple + friendly + natural explanation\n\n"
        "🟢 Bas koi bhi text / photo!",
        parse_mode="Markdown"
    )

# -----------------------------------
# CHATGPT-STYLE REPLY ENGINE
# -----------------------------------
def ai_reply(text):
    prompt = (
        "You are ChatGPT. Reply naturally, friendly, smart and helpful.\n"
        "User jis language me baat kare, usi language me jawab do.\n"
        "Tone: Simple, clean, warm, and natural — exactly like ChatGPT.\n"
        "Agar question educational ho, simple explanation + examples do.\n"
        "Agar chat ho, conversational jawab do.\n"
        "Avoid long unnecessary essays.\n\n"
        f"User: {text}\n"
        "ChatGPT:"
    )

    r = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return r.output[0].content[0].text

# -----------------------------------
# IMAGE HANDLER — OpenAI Vision
# -----------------------------------
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')

        file_id = message.photo[-1].file_id
        info = bot.get_file(file_id)
        img_data = bot.download_file(info.file_path)

        with open("q.jpg", "wb") as f:
            f.write(img_data)

        # Read as base64 for OpenAI Vision
        with open("q.jpg", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        vision_input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", 
                     "text": "Extract text from this image and solve it. Reply naturally like ChatGPT."},
                    {"type": "input_image", 
                     "image_url": f"data:image/jpeg;base64,{b64}"}
                ]
            }
        ]

        response = client.responses.create(
            model="gpt-4o-mini",
            input=vision_input
        )

        answer = response.output[0].content[0].text
        bot.reply_to(message, f"📸 Image Question Solved:\n\n{answer}", parse_mode="Markdown")

        os.remove("q.jpg")

    except Exception as e:
        bot.reply_to(message, f"Image Error: {e}")

# -----------------------------------
# VOICE HANDLER — Direct Whisper STT
# -----------------------------------
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')

        file_id = message.voice.file_id
        info = bot.get_file(file_id)
        voice_bytes = bot.download_file(info.file_path)

        with open("voice.ogg", "wb") as f:
            f.write(voice_bytes)

        # Speech-to-Text (Whisper)
        with open("voice.ogg", "rb") as audio:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio
            )

        user_text = transcript.text
        answer = ai_reply(user_text)

        bot.reply_to(
            message,
            f"🎤 Tumne bola: {user_text}\n\n🧠 ChatGPT Answer: {answer}",
            parse_mode="Markdown"
        )

        os.remove("voice.ogg")

    except Exception as e:
        bot.reply_to(message, f"Voice Error: {e}")

# -----------------------------------
# TEXT HANDLER — ChatGPT Style
# -----------------------------------
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    bot.send_chat_action(message.chat.id, 'typing')
    answer = ai_reply(message.text)
    bot.reply_to(message, answer)


print("BOT RUNNING LIKE CHATGPT...")
bot.infinity_polling()