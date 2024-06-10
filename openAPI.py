from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests
import datetime
import pandas as pd
import re  # HTML 태그 제거를 위한 정규식 라이브러리

app = FastAPI()

# NewsAPI 키
API_KEY = '1e347c3d847140fab193cd9bc5c81570'

# 뉴스 항목을 나타내는 모델
class NewsItem(BaseModel):
    source: str
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    publishedAt: str
    content: Optional[str]

def clean_text(text):
    # HTML 태그 제거
    text = re.sub('<.*?>', '', text)
    # 특수 문자 및 불필요한 문자 제거
    text = re.sub(r'[^A-Za-z0-9가-힣\s]', '', text)
    # 줄바꿈 및 공백 문자 정리
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 뉴스 검색 엔드포인트
@app.get("/news/", response_model=List[NewsItem])
def search_news(query: str, from_date: Optional[str] = None, to_date: Optional[str] = None, language: str = 'ko', sort_by: str = 'publishedAt'):
    """
    NewsAPI를 사용하여 뉴스 기사를 검색하고 결과를 반환합니다.
    
    :param query: 검색어
    :param from_date: 검색 시작 날짜 (옵션)
    :param to_date: 검색 종료 날짜 (옵션)
    :param language: 검색 언어 (기본값: 'en')
    :param sort_by: 정렬 기준 (기본값: 'publishedAt')
    :return: 뉴스 기사 목록
    """
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'from': from_date,
        'to': to_date,
        'language': language,
        'sortBy': sort_by,
        'apiKey': API_KEY
    }
    
    # API 요청
    response = requests.get(url, params=params)
    
    # 요청 실패 시 예외 발생
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from NewsAPI")
    
    data = response.json()
    articles = data.get('articles', [])
    
    # 뉴스 항목을 저장할 리스트
    news_items = []
    
    for article in articles:
        # HTML 태그 제거
        clean_description = clean_text(article.get('description', ''))
        clean_content = clean_text(article.get('content', ''))
        
        
        news_items.append(NewsItem(
            source=article['source']['name'],
            author=article.get('author'),
            title=article['title'],
            description=clean_description,
            url=article['url'],
            publishedAt=article['publishedAt'],
            content=clean_content
        ))
    
    return news_items

# 뉴스 검색 결과를 엑셀 파일로 저장하는 엔드포인트
@app.get("/news/excel/")
def save_news_to_excel(query: str, from_date: Optional[str] = None, to_date: Optional[str] = None, language: str = 'ko', sort_by: str = 'publishedAt'):
    """
    NewsAPI를 사용하여 뉴스 기사를 검색하고 결과를 엑셀 파일로 저장합니다.
    
    :param query: 검색어
    :param from_date: 검색 시작 날짜 (옵션)
    :param to_date: 검색 종료 날짜 (옵션)
    :param language: 검색 언어 (기본값: 'en')
    :param sort_by: 정렬 기준 (기본값: 'publishedAt')
    :return: 저장된 엑셀 파일의 경로
    """
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'from': from_date,
        'to': to_date,
        'language': language,
        'sortBy': sort_by,
        'apiKey': API_KEY
    }
    
    # API 요청
    response = requests.get(url, params=params)
    
    # 요청 실패 시 예외 발생
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from NewsAPI")
    
    data = response.json()
    articles = data.get('articles', [])
    
    # 뉴스 항목을 저장할 리스트
    news_items = []
    for article in articles:
        # HTML 태그 제거
        clean_description = clean_text(article.get('description', ''))
        clean_content = clean_text(article.get('content', ''))
        
        
        news_items.append({
            'source': article['source']['name'],
            'author': article.get('author'),
            'title': article['title'],
            'description': clean_description,
            'url': article['url'],
            'publishedAt': article['publishedAt'],
            'content': clean_content
        })
    
    # DataFrame 생성 및 엑셀 파일로 저장
    df = pd.DataFrame(news_items)
    dt_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_path = f'{dt_now}_{query}.xlsx'
    df.to_excel(file_path, index=False)
    
    return {"file_path": file_path}

# FastAPI 애플리케이션 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)