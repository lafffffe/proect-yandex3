import asyncio
from TikTokApi import TikTokApi
import requests

async def download_tiktok_video(video_id: str, filename: str = "video.mp4"):
    api = TikTokApi()
    video_info = await api.video(id=video_id).info()
    video_url = video_info["video"]["download_addr"]
    
    # Скачивание с заголовками (без них TikTok может вернуть 403)
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.tiktok.com/"
    }
    response = requests.get(video_url, headers=headers)
    
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Видео сохранено как {filename}!")

# Пример вызова
id = "7027795028252560642"
asyncio.run(download_tiktok_video(id))
