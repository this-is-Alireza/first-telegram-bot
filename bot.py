# import logging
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# # Bot token
# BOT_TOKEN = "8591604751:AAF2JtpBku6xigI63zrdIH-OahherAtPBXE"

# # Free public proxies (SOCKS5)
# PROXY_URLS = [
#     "http://20.210.113.32:80",
#     "http://20.206.106.192:80", 
#     "http://20.219.177.73:3129",
#     "http://43.153.74.116:3128",
#     "http://65.109.137.83:80",
#     "http://38.156.74.177:80",
#     "http://191.101.39.27:80"
# ]

# # Logging setup
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Hello! 👋 Welcome to the bot!")

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(f"You said: {update.message.text}")

# def main():
#     for proxy_url in PROXY_URLS:
#         try:
#             print(f"🔗 Trying proxy: {proxy_url}")
            
#             # Create application with proxy
#             application = Application.builder() \
#                 .token(BOT_TOKEN) \
#                 .proxy_url(proxy_url) \
#                 .build()

#             # Add handlers
#             application.add_handler(CommandHandler("start", start))
#             application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
            
#             print("🤖 Bot is connecting...")
#             application.run_polling()
#             break  # If successful, break the loop
            
#         except Exception as e:
#             print(f"❌ Proxy {proxy_url} failed: {e}")
#             continue  # Try next proxy
    
#     print("⚠️ All proxies failed!")

# if __name__ == "__main__":
#     main()





import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8591604751:AAF2JtpBku6xigI63zrdIH-OahherAtPBXE"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("salaaaaaammmm👋")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

def main():
    try:
        # بدون پروکسی - فقط با VPN
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
        print("🤖 Bot starting with VPN...")
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure your VPN is connected and working!")

if __name__ == "__main__":
    main()