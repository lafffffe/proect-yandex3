from yandex_music import Client
import re, requests, os

token = 'y0__xCDkqbMBBje-AYgk_eljBO3d4-yyfOq5NZXPCSgy375V2x-ww'
client = Client(token).init()


def blablabla(url, artists, title, duration):

    pattern = r'\/track\/(\d+)'
    match = re.search(pattern, url)
    trackID = match.group(1)
    print(trackID)
    mp3 = client.tracksDownloadInfo(track_id=trackID, get_direct_links=True)[0]['direct_link']
    print(mp3)
    #return mp3
    send_renamed_mp3(mp3, artists, title, duration)


def get_yandex_audio(url):

    if 'album' in url:
        match = re.search(r'\/album\/(\d+)', url)
        ALBUM_ID = match.group(1)
        print(ALBUM_ID)
        list = []

        album = client.albums_with_tracks(ALBUM_ID)
        tracks = []
        for i, volume in enumerate(album.volumes):
            if len(album.volumes) > 1:
                tracks.append(f'💿 Диск {i + 1}')
            tracks += volume

        for track in tracks:
            list += [track.id, track.artists, track.title, track.duration]
            if isinstance(track, str):
                print(track)
            else:
                artists = ''
                if track.artists:
                    artists = ' - ' + ', '.join(artist.name for artist in track.artists)
                print(track.title + artists)

    elif 'track' in url:
        return  ['audio', blablabla(url, )]

        print(list)
        res = ['audios', len(list)]
        for id in list:
            url2 = f'https://music.yandex.ru/album/{ALBUM_ID}/track/{id[0]}?utm_medium=copy_link'
            res.append(blablabla(url2, list[1], list[2], list[3]))
        return res


import requests
import os
from io import BytesIO

def send_renamed_mp3(mp3, artists, title, duration):
    
    # Произвольные метаданные
    custom_filename = title
    title = title
    artist = artists
    duration = duration
    
    # Скачиваем файл в оперативную память (без сохранения на диск)
    response = requests.get(mp3)
    response.raise_for_status()
    
    # Создаем файловый объект в памяти
    audio_file = BytesIO(response.content)
    audio_file.name = custom_filename  # Важно для имени при скачивании

    # Закрываем файловый объект (память очистится автоматически)
    if 'audio_file' in locals():
        audio_file.close()
    return audio_file, custom_filename, title, artist, duration


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