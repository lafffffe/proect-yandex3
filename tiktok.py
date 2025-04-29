import requests


def get_tiktok_video_url(url):
    full_url = requests.head(url, allow_redirects=True).url
    response = requests.get(f"https://www.tikwm.com/api/?url={full_url}")
    return response.json()['data']['play']
