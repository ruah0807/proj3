import requests
from bs4 import BeautifulSoup



def get_article_content(url):
    """ 주어진 URL에서 뉴스 본문을 추출합니다. """
    try:
        data = requests.get(url)
        
        soup = BeautifulSoup(data.content, 'html.parser')

        article = soup.find('article', {'id': 'dic_area'}).text.strip()
        # print(article)
        
        if article is None:
            print(f"No article content found at {url}")
            return None, None
        
        # 이미지 url 추출
        img_tag = soup.select_one('img', {'id':'img1'})  # 'article' 내의 'img' 태그 찾기
        img_url=''
        if img_tag != None:
            img_url = img_tag['data-src']
   
        return article, img_url     
       
    except Exception as e:
        print(f"An error occurred while retrieving article: {e}")
        return None, None




def convert_to_naver_news_url(finance_url):
    """ finance.naver.com 링크를 n.news.naver.com 형식의 실제 뉴스 페이지 URL로 변환합니다. """
    try:
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
    """ 주어진 종목 코드에 대해 뉴스를 크롤링하고, 각 뉴스 링크를 변환한 후 본문을 추출합니다. """
    try:
        # 증권 뉴스 URL
        url = f'https://finance.naver.com/item/news_news.naver?code={code}&page=&clusterId='
        
        data = requests.get(url)
        
        # 상태 코드 확인
        if data.status_code != 200:
            print(f"Failed to retrieve data for code {code}: {data.status_code}")
            return None
        
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
            published_at = dates[i].text.strip()
            article_url = titles[i].get('href')  # 올바른 href 속성을 추출
            if article_url:
                # 절대 URL 확인 및 변환
                if article_url.startswith('/item'):
                    article_url = 'https://finance.naver.com' + article_url
                converted_url = convert_to_naver_news_url(article_url)
                if converted_url:
                    # print(f"Converted article URL: {converted_url}")  # 디버깅을 위해 URL 출력
                    content, img_url = get_article_content(converted_url)
                    if content:
                        news_item = {
                            'title': title,
                            'content': content,
                            'author': author,
                            'publishedAt': published_at, 
                            'img_url': img_url,
                            'news_url': converted_url
                        }
                        # print(f"Appending news item: {news_item}")  # 디버깅 메시지
                        news_data.append(news_item)
                    else:
                        print(f"No content found for URL: {converted_url}")
        
        # print(f"Returning news data: {news_data}")  # 디버깅 메시지
        return news_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

