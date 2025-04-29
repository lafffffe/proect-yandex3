import requests

def get_tiktok_via_service(video_url):
    response = requests.get(f"https://www.tikwm.com/api/?url={video_url}")
    return response.json()['data']['play']



# Пример использования
url = 'https://www.tiktok.com/@spasskaia_anastasia/video/7055209182353460481?is_from_webapp=1&sender_device=pc'
direct_url = get_tiktok_via_service(url)
print(direct_url)