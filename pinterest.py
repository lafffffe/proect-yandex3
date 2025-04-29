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


def get_pinterest_image_url(pin_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(pin_url, headers=headers)
        response.raise_for_status()
        print(response.content)
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_image = soup.find("meta", property="og:image")
        if meta_image:
            return meta_image["content"]

        match = re.search(r'"images":\{"orig":\{"url":"(https:\\/\\/[^"]+)"', response.text)
        if match:
            return match.group(1).replace("\\", "")

        raise ValueError("Изображение не найдено")

    except Exception as e:
        print(f"Ошибка: {e}")
        return None


# Пример использования
pin_url = 'https://ru.pinterest.com/pin/1055390493930590965/'
image_url = get_pinterest_image_url(pin_url)
print(image_url)