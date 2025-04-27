import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup
import requests
from dowland_video.py import download_media



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)



async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я умею скачивать видео по ссылке",
    )

async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать...")

def main():
    application = Application.builder().token('7801940292:AAEEDCLRZO0f4vzTJyzEgOMNSpxQWwB-k3Q').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling()

if __name__ == '__main__':
    main()