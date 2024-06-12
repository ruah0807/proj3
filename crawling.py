import requests
from bs4 import BeautifulSoup


# def inspect_article_structure(url):
#     try:
#         response = requests.get(url)
#         if response.status_code != 200:
#             print(f"Failed to retrieve article from {url}: {response.status_code}")
#             return
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # HTML 전체 구조를 확인하기 위해 전체 출력
#         with open('article_structure.html', 'w', encoding='utf-8') as file:
#             file.write(soup.prettify())
        
#         print("HTML 구조를 article_structure.html 파일로 저장했습니다.")

#     except Exception as e:
#         print(f"An error occurred while retrieving article: {e}")

# # 예제 URL로 HTML 구조 확인
# test_url = "https://n.news.naver.com/mnews/article/011/0004352036"
# inspect_article_structure(test_url)

def get_redirected_url(url):
    try:
        response = requests.get(url, allow_redirects=True)
        
        if response.status_code == 200:
            return response.url
        else:
            print(f"Failed to retrieve redirected URL from {url}: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while retrieving redirected URL: {e}")
        return None

def get_article_content(url):
    try:
        redirected_url = get_redirected_url(url)
        if not redirected_url:
            return None
        print(f"Fetching content from redirected URL: {redirected_url}")  # 디버깅을 위해 URL 출력
        data = requests.get(redirected_url)
        if data.status_code != 200:
            print(f"Failed to retrieve article from {redirected_url}: {data.status_code}")
            return None
        soup = BeautifulSoup(data.content, 'html.parser')

        # 'div' 태그의 'id'가 'newsct_article'인 요소 내의 'article' 태그 찾기
        article_div = soup.find('div', {'id': 'newsct_article'})
        if article_div:
            article = article_div.find('article')
            if article:
                return article.text.strip()
        print(f"No article content found at {redirected_url}")
        return None
    except Exception as e:
        print(f"An error occurred while retrieving article: {e}")
        return None


def crawling(code):
    try:
        # 증권 뉴스 URL
        url = f'https://finance.naver.com/item/news_news.naver?code={code}&page=&clusterId='
        
        data = requests.get(url)
        
        # 상태 코드 확인
        if data.status_code != 200:
            print(f"Failed to retrieve data for code {code}: {data.status_code}")
            return None
        
        # soup 사용해서 html 변환
        soup = BeautifulSoup(data.content, 'html.parser')

        # 뉴스 제목, 저자, 날짜 파싱
        titles = soup.find_all('a', class_='tit')
        authors = soup.find_all('td', class_='info')
        dates = soup.find_all('td', class_='date')
        
        news_data = []
        for i in range(min(len(titles), len(authors), len(dates))):
            title = titles[i].text.strip()
            author = authors[i].text.strip()
            date = dates[i].text.strip()
            article_url = titles[i]['href']
            # 절대 URL 확인 및 변환
            if article_url.startswith('/'):
                article_url = 'https://finance.naver.com' + article_url
            elif article_url.startswith('http'):
                article_url = article_url
            else:
                article_url = 'https://n.news.naver.com' + article_url
            print(article_url)  # 디버깅을 위해 URL 출력
            content = get_article_content(article_url)
            if content:
                news_data.append((title, author, date, content))
        
        return news_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
# 종목 리스트
companies = ['000660', '196170']

# 파일에 결과 저장 (기존 내용을 유지하고 추가)
with open('a.txt', 'a') as f:
    for code in companies:
        news_list = crawling(code)
        if news_list:
            for news in news_list:
                f.write(f"{news[0]} | {news[1]} | {news[2]} \n")