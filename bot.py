import logging, re
from gc import callbacks
from pyexpat.errors import messages

from telegram import InputMediaPhoto, InputFile
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ApplicationBuilder
from telegram.constants import ParseMode
from telegram import ReplyKeyboardMarkup, Bot
import requests
from dowland_video import download_media
from io import BytesIO

with open('apiBot.txt', 'r') as file:
    tokenBot = file.readline().strip()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я умею скачивать видео по ссылке",
        reply_markup=None
    )


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать...")


async def extract_mp3_url(yandex_url):
    """Получаем прямую ссылку на MP3 из Яндекс.Музыки"""
    # Здесь нужно использовать API Яндекс.Музыки или парсить страницу
    # Это примерная логика (реализация зависит от вашего метода получения MP3)
    return "https://example.com/real-mp3-link.mp3"  # Замените на реальную логику


async def detect_metadata(audio_data, yandex_url):
    """Определяем метаданные: 1) Из ID3 тегов 2) Из URL Яндекс.Музыки"""
    try:
        # Пробуем прочитать ID3 теги
        audio = MP3(audio_data, ID3=ID3)
        title = audio.get("TIT2", "").text[0] if "TIT2" in audio else ""
        artist = audio.get("TPE1", "").text[0] if "TPE1" in audio else ""

        # Если тегов нет, пробуем извлечь из URL
        if not title or not artist:
            track_id = re.search(r'track/(\d+)', yandex_url).group(1)
            title, artist = await fetch_from_yandex_api(track_id)  # Нужен API доступ

        return title or "Неизвестный трек", artist or "Неизвестный исполнитель"
    except:
        return "Неизвестный трек", "Неизвестный исполнитель"


async def fetch_from_yandex_api(track_id):
    """Получаем данные через API Яндекс.Музыки (нужна реализация)"""
    return "Название трека", "Исполнитель"  # Заглушка

async def downloadLink(update, context):
    url = update.message.text
    link = download_media(url)
    if link[0] == 'photo':
        await context.bot.send_photo(update.message.chat_id, link[1])

    elif link[0] == 'photoes':
        media_group = [InputMediaPhoto(url) for url in link[2]]
        n = link[1]//10
        ind = 0
        for i in range(n):
            await context.bot.send_media_group(update.message.chat_id, media_group[ind:ind+10])
            ind += 10
        await context.bot.send_media_group(update.message.chat_id, media_group[ind:])

    elif link[0] == 'video':

        await context.bot.send_video(update.message.chat_id, link[1])

    elif link[0] == 'audio':
        audio_file = link[1]
        custom_filename = link[2]
        title = link[3]
        artist = link[4]

        await context.bot.send_audio(
            chat_id=update.message.chat_id,
            audio=InputFile(audio_file, filename=custom_filename),
            title=title,
            performer=artist,
            duration=0  # Можно указать реальную длину, если известна
        )
        if 'audio_file' in locals():
            audio_file.close()


    elif link[0] == 'audios':
        
        for i in range(2, link[1] + 2):
            audio_file = link[i][0]
            custom_filename = link[i][1]
            title = link[i][2]
            artist = link[i][3]

            await context.bot.send_audio(
                chat_id=update.message.chat_id,
                audio=InputFile(audio_file, filename=custom_filename),
                title=title,
                performer=artist,
                duration=0  # Можно указать реальную длину, если известна
            )
            if 'audio_file' in locals():
                audio_file.close()

    elif link[0] == "audios_pl":

        for i in range(2, link[1] + 3):

            audio_file = link[i][0]
            custom_filename = link[i][1]
            title = link[i][2]
            artist = link[i][3]

            await context.bot.send_audio(
            chat_id=update.message.chat_id,
            audio=InputFile(audio_file, filename=custom_filename),
            title=title,
            performer=artist,
            duration=0  # Можно указать реальную длину, если известна
            )
        if 'audio_file' in locals():
            audio_file.close()


    elif link[0] == 'error':
        await context.bot.send_message(update.message.chat_id, link[1])


def main():
    #application = Application.builder().token(tokenBot).build()
    application = ApplicationBuilder().token(tokenBot).read_timeout(50).write_timeout(50).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT, downloadLink))

    application.run_polling()


if __name__ == '__main__':
    main()