import logging
from gc import callbacks
from pyexpat.errors import messages

from telebot.types import InputMediaPhoto

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
    url = update.message.text
    link = download_media(url)
    if link[0] == 'photo':
        await context.bot.send_photo(update.message.chat_id, link[1])
    elif link[0] == 'photoes':
        media_group = [
            InputMediaPhoto(media=url)
            for i, url in enumerate(link[2])
        ]
        await context.bot.send_media_group(update.message.chat_id, media_group)
    elif link[0] == 'video':
        await context.bot.send_video(update.message.chat_id, link[1])
    elif link[0] == 'error':
        await context.bot.send_message(update.message.chat_id, link[1])


def main():
    application = Application.builder().token('7801940292:AAEEDCLRZO0f4vzTJyzEgOMNSpxQWwB-k3Q').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT, downloadLink))

    application.run_polling()


if __name__ == '__main__':
    main()
