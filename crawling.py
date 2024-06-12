import requests
from bs4 import BeautifulSoup

def get_article_content(url):
    try:
        print(f"Fetching content from URL: {url}")  # 디버깅을 위해 URL 출력
        data = requests.get(url)
        if data.status_code != 200:
            print(f"Failed to retrieve article from {url}: {data.status_code}")
            return None
        soup = BeautifulSoup(data.content, 'html.parser')

        # 'div' 태그의 'id'가 'newsct_article'인 요소 내의 'article' 태그 찾기
        article_div = soup.find('div', {'id': 'newsct_article'})
        if article_div:
            article = article_div.find('article')
            if article:
                return article.text.strip()
        print(f"No article content found at {url}")
        return None
    except Exception as e:
        print(f"An error occurred while retrieving article: {e}")
        return None

def convert_to_naver_news_url(finance_url):
    try:
        # URL 예시: https://finance.naver.com/item/news_read.naver?article_id=0002879618&office_id=029&code=196170&page=&sm=
        parts = finance_url.split('?')[1].split('&')
        params = {part.split('=')[0]: part.split('=')[1] for part in parts}
        article_id = params.get('article_id')
        office_id = params.get('office_id')
        if article_id and office_id:
            return f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}"
        else:
            print(f"Invalid article ID or office ID in URL: {finance_url}")
            return None
    except Exception as e:
        print(f"An error occurred while converting URL: {e}")
        return None

def crawling(code):
    try:
        # 증권 뉴스 URL
        url = f'https://finance.naver.com/item/news_news.naver?code={code}&page=&clusterId='
        print(f"Fetching news list from URL: {url}")  # 디버깅을 위해 URL 출력
        
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

        print(f"Found {len(titles)} titles, {len(authors)} authors, and {len(dates)} dates.")  # 디버깅 메시지
        
        news_data = []
        for i in range(min(len(titles), len(authors), len(dates))):
            title = titles[i].text.strip()
            author = authors[i].text.strip()
            date = dates[i].text.strip()
            article_url = titles[i].get('href')  # 올바른 href 속성을 추출
            print(f"Raw article URL: {article_url}")  # 디버깅을 위해 원본 URL 출력
            if article_url:
                # 절대 URL 확인 및 변환
                if article_url.startswith('/item'):
                    article_url = 'https://finance.naver.com' + article_url
                converted_url = convert_to_naver_news_url(article_url)
                if converted_url:
                    print(f"Converted article URL: {converted_url}")  # 디버깅을 위해 URL 출력
                    content = get_article_content(converted_url)
                    if content:
                        news_data.append((title, author, date, content))
                    else:
                        print(f"No content found for URL: {converted_url}")
                    
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
                f.write(f"{news[0]} | {news[1]} | {news[2]} | {news[3]}\n")