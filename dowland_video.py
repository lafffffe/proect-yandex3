import os
import re
import yt_dlp
import requests
from bs4 import BeautifulSoup


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
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        print(f"✅ TikTok видео скачано: {filename}")
        return filename


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
    """Скачивает фото или видео из Pinterest с правильным определением типа"""
    output_dir = create_download_dir(output_dir)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text

        # === 1. Пытаемся найти видео (приоритет) ===
        video_url = None

        # Вариант 1: Ищем в JSON (новый Pinterest)
        video_match = re.search(r'"video_list":\{"V_720P":\{"url":"(https://[^"]+\.mp4)"', html)
        if video_match:
            video_url = video_match.group(1).replace("\\", "")

        # Вариант 2: Ищем в HTML (старый Pinterest)
        else:
            soup = BeautifulSoup(html, 'html.parser')
            video_tag = soup.find("video")
            if video_tag and video_tag.get("src"):
                video_url = video_tag["src"]

        # Если нашли видео — скачиваем
        if video_url:
            return download_pinterest_video(video_url, output_dir)

        # === 2. Если видео нет, ищем фото ===
        photo_url = None

        # Вариант 1: Ищем в <meta property="og:image"> (обычно здесь основное фото)
        meta_image = re.search(r'<meta property="og:image" content="(https://[^"]+)"', html)
        if meta_image:
            photo_url = meta_image.group(1)

        # Вариант 2: Ищем в JSON (для галерей)
        else:
            image_match = re.search(r'"images":\{"orig":\{"url":"(https://[^"]+)"', html)
            if image_match:
                photo_url = image_match.group(1).replace("\\", "")

        # Если нашли фото — скачиваем
        if photo_url:
            return download_pinterest_photo(photo_url, output_dir)

        # Если ничего не нашли
        raise ValueError("Не удалось найти ни видео, ни фото на странице")

    except Exception as e:
        print(f"❌ Ошибка при загрузке Pinterest: {e}")
        return None


def download_pinterest_video(video_url, output_dir):
    """Скачивает видео с Pinterest"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        video_data = requests.get(video_url, headers=headers).content
        filename = os.path.join(output_dir, f"pinterest_video_{os.path.basename(video_url)[:10]}.mp4")

        with open(filename, "wb") as f:
            f.write(video_data)

        print(f"✅ Pinterest видео скачано: {filename}")
        return video_data
    except Exception as e:
        print(f"❌ Ошибка при скачивании видео: {e}")
        return None


def download_pinterest_photo(photo_url, output_dir):
    """Скачивает фото с Pinterest"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        photo_data = requests.get(photo_url, headers=headers).content
        filename = os.path.join(output_dir, f"pinterest_photo_{os.path.basename(photo_url)[:10]}.jpg")

        with open(filename, "wb") as f:
            f.write(photo_data)

        print(f"✅ Pinterest фото скачано: {filename}")
        return photo_data
    except Exception as e:
        print(f"❌ Ошибка при скачивании фото: {e}")
        return None


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
