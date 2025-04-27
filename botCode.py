import logging
from gc import callbacks
from pyexpat.errors import messages

from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup, Bot
import requests
from dowland_video import download_media

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

async def downloadLink(update, context):
    link = update.message.text
    filename = download_media(link)
    with open(f'{filename}', "rb") as video_file:
        await context.bot.send_video(chat_id=update.message.chat_id, video=video_file)


def main():
    application = Application.builder().token('7801940292:AAEEDCLRZO0f4vzTJyzEgOMNSpxQWwB-k3Q').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT, downloadLink))

    application.run_polling()

if __name__ == '__main__':
    main()