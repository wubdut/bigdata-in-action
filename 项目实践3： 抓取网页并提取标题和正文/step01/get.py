import requests
url = "https://news.sina.com.cn "
html = requests.get(url)
print(html)