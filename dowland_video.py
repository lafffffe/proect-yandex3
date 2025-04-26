import yt_dlp


def download_tiktok_video_ytdlp(url, output_path="C:\\Users\\dimag\\OneDrive\\Документы\\proect-yandex3\\files\\downloaded_video.mp4"):
    ydl_opts = {
        'outtmpl': output_path,  # Путь для сохранения
        'format': 'best',  # Лучшее качество
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print(f"Видео скачано: {output_path}")
        return output_path

# Пример использования
#tiktok_url = "https://www.tiktok.com/@evvagner/video/7038602594289290498?is_from_webapp=1&sender_device=pc"
#download_tiktok_video_ytdlp(tiktok_url)