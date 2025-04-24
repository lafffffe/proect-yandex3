import yt_dlp


def download_tiktok_video_ytdlp(url, output_path="downloaded_video.mp4"):
    ydl_opts = {
        'outtmpl': output_path,  # Путь для сохранения
        'format': 'best',  # Лучшее качество
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print(f"Видео скачано: {output_path}")


# Пример использования
tiktok_url = "https://www.tiktok.com/@username/video/1234567890"
download_tiktok_video_ytdlp(tiktok_url)