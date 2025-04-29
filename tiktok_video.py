import os, yt_dlp

def get_tiktok_video_url(url):
    """Скачивает видео из TikTok через yt-dlp"""

    ydl_opts = {
            'format': 'best',
            'quiet': True
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(info)
        return info