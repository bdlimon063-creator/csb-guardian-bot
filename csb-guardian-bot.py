import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from openai import OpenAI

# ================== CONFIG ==================
TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# ================== AI REPLY ==================
async def ai_reply(prompt: str) -> str:
    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are a friendly Bangla-English Telegram group assistant."},
                {"role":"user","content":prompt}
            ],
            max_tokens=150
        )
        return r.choices[0].message.content.strip()
    except Exception:
        return "🙂 আমি সাহায্য করার জন্য আছি। একটু পরিষ্কার করে বলো।"

# ================== MAIN HANDLER ==================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Auto reply for "আমি তুইরি করলাম"
    if "আমি তুইরি করলাম" in text.lower():
        await update.message.reply_text("আমার স্যার CSB~BANGLADESH")
        return

    # AI reply
    reply = await ai_reply(text)
    await update.message.reply_text(reply)

# ================== RUN BOT ==================
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 CSB Guardian Bot is running...")
app.run_polling()
