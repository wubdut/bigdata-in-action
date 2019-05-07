import requests
from bs4 import BeautifulSoup

url = "https://news.sina.com.cn"
html = requests.get(url)
soup = BeautifulSoup(html.content, 'lxml')
print(soup.title)

for link in soup.select("div.ct_t_01 h1 a"):
    print(link.get("href"))