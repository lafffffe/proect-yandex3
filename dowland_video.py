import re
import requests
from bs4 import BeautifulSoup

from pinterest import get_pinterest_image_url
from tiktok import get_tiktok_video_url
from youtube import get_youtube_video_url


def download_tiktok_media(url):
    response = requests.head(url, allow_redirects=True)
    url = response.url

    if "/photo/" in url:
        return ['photo', download_tiktok_photo(url)]
    else:
        return ['video', get_tiktok_video_url(url)]


def download_tiktok_photo(url):
    """Скачивает фото из TikTok (парсинг HTML)"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Поиск URL изображения в JSON-данных
    match = re.search(r'"images":\["(https:[^"]+)"\]', response.text)
    if not match:
        raise ValueError("Не удалось найти изображение")

    img_url = match.group(1).replace("\\u002F", "/")
    img_data = requests.get(img_url, headers=headers).content

    return img_data


def download_pinterest_media(url):
    link = get_pinterest_image_url(url)

    return ['photo', link]


def download_media(url):
    """Определяет платформу и скачивает контент"""
    if "youtube.com" in url or "youtu.be" in url:
        return ['video', get_youtube_video_url(url)]
    elif "tiktok.com" in url:
        return download_tiktok_media(url)
    elif "pinterest." in url:
        return download_pinterest_media(url)
    else:
        print("❌ Неподдерживаемая платформа")
        return ['error', '❌ Неподдерживаемая платформа']
