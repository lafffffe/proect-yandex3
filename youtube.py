import yt_dlp
import requests


def get_youtube_video_url(url):

    response = requests.head(url, allow_redirects=True)
    url = response.url

    ydl_opts = {
        'format': 'best',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print('#############' * 15)
        print(url)
        info = ydl.extract_info(url, download=True)
        print()
        print('#############' * 15)
        return ['video', info]