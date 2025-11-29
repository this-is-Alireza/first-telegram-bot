import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = "8591604751:AAF2JtpBku6xigI63zrdIH-OahherAtPBXE"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("salaaaaaammmm👋")

def echo(update: Update, context: CallbackContext):
    update.message.reply_text(f"You said: {update.message.text}")

def main():
    try:
        # ایجاد Updater به جای Application
        updater = Updater(BOT_TOKEN, use_context=True)
        
        # گرفتن dispatcher
        dp = updater.dispatcher
        
        # اضافه کردن handlerها
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
        
        print("🤖 Bot starting...")
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
