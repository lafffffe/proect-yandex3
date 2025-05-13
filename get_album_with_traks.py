import os
import re
from yandex_music import Client

# без авторизации недоступен список треков альбома
TOKEN = os.environ.get('y0__xCgg-f6Bhje-AYgnZedjBOrjl44G004DFTLubtv0VE_ced6Pg')
url = 'https://music.yandex.ru/album/35098588?utm_medium=copy_linkk'
match = re.search(r'\/album\/(\d+)', url)
ALBUM_ID = match.group(1)
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
list = []

for track in tracks:
    list += [track.id]
    if isinstance(track, str):
        print(track)
    else:
        artists = ''
        if track.artists:
            artists = ' - ' + ', '.join(artist.name for artist in track.artists)
        print(track.title + artists)
print(list)
for id in list:
    url2 = f'https://music.yandex.ru/album/{ALBUM_ID}/track/{id}?utm_medium=copy_link'
    print(url2)