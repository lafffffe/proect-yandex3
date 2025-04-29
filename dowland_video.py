import re
import requests
from bs4 import BeautifulSoup

from pinterest import get_pinterest_image_url
from tiktok import get_tiktok_video_url, get_tiktok_photoes_url
from youtube import get_youtube_video_url


def download_tiktok_media(url):
    response = requests.head(url, allow_redirects=True)
    url = response.url

    if "/photo/" in url:
        return get_tiktok_photoes_url(url)
    else:
        return get_tiktok_video_url(url)



def download_pinterest_media(url):
    link = get_pinterest_image_url(url)

    return ['photo', link]


def download_media(url):
    """Определяет платформу и скачивает контент"""
    if "youtube.com" in url or "youtu.be" in url:
        return ['video', get_youtube_video_url(url)]
    elif "tiktok.com" in url:
        return download_tiktok_media(url)
    elif "pinterest." in url or 'pin.it' in url:
        return download_pinterest_media(url)
    else:
        return ['error', '❌ Неподдерживаемая платформа']
