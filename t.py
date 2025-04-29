import requests

url = 'https://vt.tiktok.com/ZShejXtvv/'
full_url = requests.head(url, allow_redirects=True).url
response = requests.get(f"https://www.tikwm.com/api/?url={full_url}")

print(response.json()['data']['images'])