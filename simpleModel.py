from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

TOKEN = '8307611638:AAEECNiVEaxK5SmG3p0ZMk6UQ442VHp6hZU'
MODEL_NAME = "deepseek-ai/deepseek-llm-7b-base"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Отправь мне текст.')

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    result = user_text.lower()
    inputs = tokenizer(result, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=150, 
            do_sample=True, 
            temperature=0.7, 
            top_p=0.95
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    await update.message.reply_text(decoded)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, device_map="auto")
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()
