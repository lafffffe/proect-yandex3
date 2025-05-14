from yandex_music import Client
import re, requests, os
import time

token = 'y0__xCDkqbMBBje-AYgk_eljBO3d4-yyfOq5NZXPCSgy375V2x-ww'
client = Client(token).init()


def blablabla(url, artists, title):

    pattern = r'\/track\/(\d+)'
    match = re.search(pattern, url)
    trackID = match.group(1)
    mp3 = client.tracksDownloadInfo(track_id=trackID, get_direct_links=True)[0]['direct_link']
    #return mp3
    return send_renamed_mp3(mp3, artists, title)


def get_yandex_audio(url):

    if 'track' in url:
        match = re.search(r'\/album\/(\d+)', url)
        ALBUM_ID = match.group(1)

        album = client.albums_with_tracks(ALBUM_ID)

        pattern = r'\/track\/(\d+)'
        match = re.search(pattern, url)
        trackID = match.group(1)

        artist = 'name'
        title = 'music'

        for i, volume in enumerate(album.volumes):
            if volume[0].id == trackID:
                artist = volume[0].artists[0].name
                title = volume[0].title
                break

        return  ['audio', *blablabla(url, artist, title)]
    elif 'album' in url:
        match = re.search(r'\/album\/(\d+)', url)
        ALBUM_ID = match.group(1)
        list = []

        album = client.albums_with_tracks(ALBUM_ID)
        tracks = []
        for i, volume in enumerate(album.volumes):
            if len(album.volumes) > 1:
                tracks.append(f'💿 Диск {i + 1}')
            tracks += volume

        for track in tracks:
            list += [(track.id, track.artists[0].name, track.title)]
            '''
            if isinstance(track, str):
                print(track)
            else:
                artists = ''
                if track.artists:
                    artists = ' - ' + ', '.join(artist.name for artist in track.artists)
                print(track.title + artists)'''
        res = ['audios', len(list)]
        for i in range(len(list)):
            url2 = f'https://music.yandex.ru/album/{ALBUM_ID}/track/{list[i][0]}?utm_medium=copy_link'
            res += [blablabla(url2, list[i][1], list[i][2])]
        return res
    
    elif 'playlist' in url:
        token = 'y0__xCDkqbMBBje-AYgk_eljBO3d4-yyfOq5NZXPCSgy375V2x-ww'
        client = Client(token).init()
        parts = url.split('/')
        username = parts[4]
        playlist_id = parts[6].split('?')[0]
        # Получаем плейлист через новый API метод
        playlist = client.users_playlists(playlist_id, user_id=username)

        if not playlist:
            raise Exception("Плейлист не найден или доступ запрещен")

        # Получаем полную информацию о треках
        track_ids = [track.track_id for track in playlist.tracks]
        tracks = client.tracks(track_ids)
        res = []
        for track in tracks:
            try:
                time.sleep(1)
                download_info = track.get_download_info()
                mp3_info = next((i for i in download_info if i.codec == 'mp3'), None)

                # Получаем прямую ссылку
                mp3_url = mp3_info.get_direct_link()

                res += [send_renamed_mp3(mp3_url, track.artists[0]["name"], track.title)]

            except yandex_music.exceptions.UnauthorizedError:
                print("Ошибка авторизации. Пробуем переподключиться...")
                client = Client(token).init()  # Переавторизация
                continue
            except Exception as e:
                print(f"Ошибка при обработке трека: {e}")
                continue
        return ["audios_pl", len(res) - 1] + res



import requests
import os
from io import BytesIO

def send_renamed_mp3(mp3, artists, title):
    
    # Произвольные метаданные
    custom_filename = title
    title = title
    artist = artists
    
    # Скачиваем файл в оперативную память (без сохранения на диск)
    response = requests.get(mp3)
    response.raise_for_status()
    
    # Создаем файловый объект в памяти
    audio_file = BytesIO(response.content)
    audio_file.name = custom_filename  # Важно для имени при скачивании
    #audio_file2 = audio_file

    # Закрываем файловый объект (память очистится автоматически)
    #if 'audio_file' in locals():
    #    audio_file.close()
    return audio_file, custom_filename, title, artist


# TOKEN = os.environ.get('y0__xCgg-f6Bhje-AYgnZedjBOrjl44G004DFTLubtv0VE_ced6Pg')
# url = 'https://music.yandex.ru/album/35098588?utm_medium=copy_linkk'
# match = re.search(r'\/album\/(\d+)', url)
# ALBUM_ID = match.group(1)
# print(ALBUM_ID)
#
# client = Client(TOKEN).init()
#
# album = client.albums_with_tracks(ALBUM_ID)
# tracks = []
# for i, volume in enumerate(album.volumes):
#     if len(album.volumes) > 1:
#         tracks.append(f'💿 Диск {i + 1}')
#     tracks += volume
#
# text = 'АЛЬБОМ\n\n'
# text += f'{album.title}\n'
# text += f"Исполнитель: {', '.join([artist.name for artist in album.artists])}\n"
# text += f'{album.year} · {album.genre}\n'
#
# cover = album.cover_uri
# if cover:
#     text += f'Обложка: {cover.replace("%%", "400x400")}\n\n'
#
# text += 'Список треков:'
#
# print(text)
# list = []
#
# for track in tracks:
#     list += [track.id]
#     if isinstance(track, str):
#         print(track)
#     else:
#         artists = ''
#         if track.artists:
#             artists = ' - ' + ', '.join(artist.name for artist in track.artists)
#         print(track.title + artists)
# print(list)
# for id in list:
#     url2 = f'https://music.yandex.ru/album/{ALBUM_ID}/track/{id}?utm_medium=copy_link'
#     print(url2)

# a = get_yandex_audio('https://music.yandex.ru/album/36417583/track/138670465?utm_medium=copy_link')
# print(a)