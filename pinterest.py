# import requests, json
# url = 'https://ru.pinterest.com/pin/556124254006368981/'
# response = requests.head(url, allow_redirects=True)
#
#
# url = response.url
# response = requests.get(url)
# image_url = response.json()["image_original_url"]
# print(image_url)

import requests
from bs4 import BeautifulSoup
import re


def get_pinterest_media_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        full_url = requests.head(url, allow_redirects=True).url
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        print(response.content)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Пытаемся найти видео сначала
        # Поиск видео URL в HTML

        video_url = re.search(r'https?://[^"]+\.mp4', response.text)
        #print("###################"* 10)
        #print(video_url[0])
        if video_url:
            return ["video", video_url[0]]
        
        # Если видео не найдено, ищем изображение
        meta_image = soup.find("meta", property="og:image")
        if meta_image:
            return ["photo", meta_image["content"]]

        match = re.search(r'"images":\{"orig":\{"url":"(https:\\/\\/[^"]+)"', response.text)
        if match:
            return ["photo", match.group(1).replace("\\", "")]

        raise ValueError("Изображение не найдено")

    except Exception as e:
        return ['error', f'❌ ошибка {e}, попробуйте еще раз']

#print(get_pinterest_media_url("https://pin.it/2D0ZpeFMb"))
# pin_url = 'https://ru.pinterest.com/pin/1055390493930590965/'
# image_url = get_pinterest_image_url(pin_url)
# print(image_url)