import re
import json
import requests
from bs4 import BeautifulSoup

def get_rutube_video_url(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    response = requests.get(url, headers=headers)
    print(response.content)
    html_content = response.text
    try:
        # Метод 1: Поиск JSON-конфига
        pattern = re.compile(r'window\.config\s*=\s*({.*?});', re.DOTALL)
        match = pattern.search(html_content)
        # print(match)
        if match:
            config = json.loads(match.group(1))
            # Проверяем разные возможные пути в JSON
            video_url = (
                config.get('video', {}).get('url') or
                config.get('player', {}).get('video', {}).get('url') or
                config.get('media', {}).get('sources', [{}])[0].get('url')
            )
            if video_url:
                return ["video", video_url]

        # Метод 2: Поиск через Open Graph мета-теги
        soup = BeautifulSoup(html_content, 'html.parser')
        meta_tag = soup.find('meta', property='og:video:url')
        # print(meta_tag)
        if meta_tag:
            # print(meta_tag.get('content'))
            return ["video", meta_tag.get('content')]

        # Метод 3: Поиск прямых ссылок в iframe/script
        iframe_pattern = re.compile(r'<iframe.*?src="(https?://rutube\.ru/embed/.*?)"')
        iframe_match = iframe_pattern.search(html_content)
        if iframe_match:
            # print(iframe_match.group(1))
            return ["video", iframe_match.group(1)]

    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Ошибка парсинга: {e}")
    return None


print(get_rutube_video_url("https://rutube.ru/play/embed/30be4376d2c8b7dd23de9cef0664e214"))
'''
# Пример использования с имитацией браузера
url = "https://rutube.ru/video/ваше_видео/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
html_content = response.text

video_url = get_rutube_video_url(html_content)

if video_url:
    print("URL видео:", video_url)
else:
    print("Ссылка не найдена. Возможные причины:")
    print("- Страница требует JavaScript (используйте Selenium)")
    print("- Rutube изменил структуру HTML")
    print("- URL видео недоступен публично")'''