import os
import re
import yt_dlp
import requests
from bs4 import BeautifulSoup

from pinterest_image import get_pinterest_image_url
from tiktok_video import get_tiktok_video_url


# ===== Общие функции =====
def create_download_dir(output_dir="downloads"):
    """Создаёт папку для загрузок, если её нет"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


# ===== TikTok =====
def download_tiktok_media(url, output_dir="downloads"):
    """Скачивает видео или фото из TikTok"""
    output_dir = create_download_dir(output_dir)

    response = requests.head(url, allow_redirects=True)
    url = response.url

    # Если это фото (проверяем по URL)
    if "/photo/" in url:
        return download_tiktok_photo(url, output_dir)
    # Если это видео
    else:
        return download_tiktok_video(url, output_dir)


def download_tiktok_photo(url, output_dir):
    """Скачивает фото из TikTok (парсинг HTML)"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Поиск URL изображения в JSON-данных
        match = re.search(r'"images":\["(https:[^"]+)"\]', response.text)
        if not match:
            raise ValueError("Не удалось найти изображение")

        img_url = match.group(1).replace("\\u002F", "/")
        img_data = requests.get(img_url, headers=headers).content

        filename = os.path.join(output_dir, f"tiktok_photo_{os.path.basename(img_url)[:10]}.jpg")
        with open(filename, "wb") as f:
            f.write(img_data)

        print(f"✅ TikTok фото скачано: {filename}")
        return img_data

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None


def download_tiktok_video(url, output_dir):
    """Скачивает видео из TikTok через yt-dlp"""
    link = get_tiktok_video_url(url)

    return ['video', link]


# ===== YouTube =====
def download_youtube_video(url, output_dir="downloads"):
    """Скачивает видео с YouTube"""
    output_dir = create_download_dir(output_dir)

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        print(f"✅ YouTube видео скачано: {filename}")
        return info


# ===== Pinterest =====
def download_pinterest_media(url, output_dir="downloads"):

    link = get_pinterest_image_url(url)

    return ['photo', link]




# ===== Главная функция =====
def download_media(url, output_dir="downloads"):
    """Определяет платформу и скачивает контент"""
    if "youtube.com" in url or "youtu.be" in url:
        return download_youtube_video(url, output_dir)
    elif "tiktok.com" in url:
        return download_tiktok_media(url, output_dir)
    elif "pinterest." in url:
        return download_pinterest_media(url, output_dir)
    else:
        print("❌ Неподдерживаемая платформа")
        return None
