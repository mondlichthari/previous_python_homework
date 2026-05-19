import requests
from bs4 import BeautifulSoup

url = "https://paper.people.com.cn/rmrb/pc/content/202512/11/content_30119677.html"
headers = {"User-Agent": "Mozilla/5.0"}

resp = requests.get(url, headers=headers)
resp.encoding = "utf-8"
soup = BeautifulSoup(resp.text, "html.parser")

# 标题
title_tag = soup.find("h1")
title = title_tag.get_text(strip=True) if title_tag else ""

paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
content = "\n".join(paragraphs)

print("标题：", title)
print("\n正文：")
print(content)
