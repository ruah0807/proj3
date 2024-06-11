import requests
from bs4 import BeautifulSoup

# IMDB의 영화 리뷰 페이지 URL
data = requests.get('https://news.naver.com/section/101')
soup = BeautifulSoup(data.content, 'html.parser')

headline = soup.select('div.sa_text a strong.sa_text_strong')[0].text

print(headline)
# # 리뷰 텍스트를 찾기
# review_divs = soup.find_all('div', class_='text show-more__control')
# for review in review_divs:
#     print(review.text)


