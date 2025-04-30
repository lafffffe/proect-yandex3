import requests, re


url = 'https://ru.pinterest.com/pin/1055390493930590965/'
session = requests.Session()
full_url = session.head(url, allow_redirects=True).url
# response = requests.get(full_url)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.pinterest.com/"
}

response = session.get(full_url, headers=headers)
response.raise_for_status()
html = response.text

# Ищем видео в JSON-данных
video_match = re.search(r'"video_list":\{"V_720P":\{"url":"(https://[^"]+\.mp4)"', html)
print(video_match)
if video_match:
    video_url = video_match.group(1).replace("\\", "")
    print(video_url)

