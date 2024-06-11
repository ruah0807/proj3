import requests
from bs4 import BeautifulSoup

# IMDB의 영화 리뷰 페이지 URL
data = requests.get('https://finance.naver.com/item/news_news.naver?code=000660&page=&clusterId=')
soup = BeautifulSoup(data.content, 'html.parser')

headline = soup.select('td.title a.tit')[0].text

print(headline)

