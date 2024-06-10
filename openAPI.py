from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import requests
import datetime
import pandas as pd 

app = FastAPI()

# NewsAPI 키
API_KEY = '1e347c3d847140fab193cd9bc5c81570'

class NewsItem(BaseModel):
    source: str
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    publishedAt: str
    content: Optional[str]

@app.get("/news/", response_model=List[NewsItem])
def search_news(query: str, from_date: Optional[str] = None, to_date: Optional[str] = None, language: str = 'en', sort_by: str = 'publishedAt'):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'from': from_date,
        'to': to_date,
        'language': language,
        'sortBy': sort_by,
        'apiKey': API_KEY
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from NewsAPI")
    
    data = response.json()
    articles = data.get('articles', [])
    
    news_items = []
    for article in articles:
        news_items.append(NewsItem(
            source=article['source']['name'],
            author=article.get('author'),
            title=article['title'],
            description=article.get('description'),
            url=article['url'],
            publishedAt=article['publishedAt'],
            content=article.get('content')
        ))
    
    return news_items

@app.get("/news/excel/")
def save_news_to_excel(query: str, from_date: Optional[str] = None, to_date: Optional[str] = None, language: str = 'en', sort_by: str = 'publishedAt'):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'from': from_date,
        'to': to_date,
        'language': language,
        'sortBy': sort_by,
        'apiKey': API_KEY
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from NewsAPI")
    
    data = response.json()
    articles = data.get('articles', [])
    
    news_items = []
    for article in articles:
        news_items.append({
            'source': article['source']['name'],
            'author': article.get('author'),
            'title': article['title'],
            'description': article.get('description'),
            'url': article['url'],
            'publishedAt': article['publishedAt'],
            'content': article.get('content')
        })
    
    df = pd.DataFrame(news_items)
    dt_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_path = f'{dt_now}_{query}.xlsx'
    df.to_excel(file_path, index=False)
    
    return {"file_path": file_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)