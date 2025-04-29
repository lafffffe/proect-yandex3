import requests


def get_tiktok_video_url(url):
    try:
        full_url = requests.head(url, allow_redirects=True).url
        response = requests.get(f"https://www.tikwm.com/api/?url={full_url}")
        return ['video', response.json()['data']['play']]
    except Exception as e:
        return ['error', f'❌ ошибка {e}, попробуйте еще раз']


def get_tiktok_photoes_url(url):
    try:
        full_url = requests.head(url, allow_redirects=True).url
        response = requests.get(f"https://www.tikwm.com/api/?url={full_url}")
        images = response.json()['data']['images']
        return ['photoes', len(images), images]
    except Exception as e:
        return ['error', f'❌ ошибка {e}, попробуйте еще раз']

# Пример использования
url = 'https://www.tiktok.com/@spasskaia_anastasia/video/7055209182353460481?is_from_webapp=1&sender_device=pc'
direct_url = get_tiktok_video_url(url)
print(direct_url)
