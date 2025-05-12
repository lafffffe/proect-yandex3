import os

from yandex_music import Client

# без авторизации недоступен список треков альбома
TOKEN = os.environ.get('y0__xCgg-f6Bhje-AYgnZedjBOrjl44G004DFTLubtv0VE_ced6Pg')
url = 'https://music.yandex.ru/album/22200537/track/103651762?utm_medium=copy_link'
ALBUM_ID = url.split('/')[4]
print(ALBUM_ID)

client = Client(TOKEN).init()

album = client.albums_with_tracks(ALBUM_ID)
tracks = []
for i, volume in enumerate(album.volumes):
    if len(album.volumes) > 1:
        tracks.append(f'💿 Диск {i + 1}')
    tracks += volume

text = 'АЛЬБОМ\n\n'
text += f'{album.title}\n'
text += f"Исполнитель: {', '.join([artist.name for artist in album.artists])}\n"
text += f'{album.year} · {album.genre}\n'

cover = album.cover_uri
if cover:
    text += f'Обложка: {cover.replace("%%", "400x400")}\n\n'

text += 'Список треков:'

print(text)

for track in tracks:
    print(track.download_info)
    print('#########################################################')
    if isinstance(track, str):
        print(track)
    else:
        artists = ''
        if track.artists:
            artists = ' - ' + ', '.join(artist.name for artist in track.artists)
        print(track.title + artists)