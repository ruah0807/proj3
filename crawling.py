import requests
from bs4 import BeautifulSoup

# IMDB의 영화 리뷰 페이지 URL
url = 'https://openapi.naver.com/v1/search/news.json?query={}' 

# 웹 페이지 요청
response = requests.get(url)

# 요청이 성공했는지 확인
if response.status_code == 200:
    # 페이지 내용 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 리뷰 텍스트를 찾기
    review_divs = soup.find_all('div', class_='text show-more__control')
    for review in review_divs:
        print(review.text)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
