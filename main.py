from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
import os
from crawling import crawling  # crawling 모듈을 import

# .env 파일의 변수를 프로그램 환경변수에 추가
load_dotenv()

DB_ID = os.getenv('DB_ID')
DB_PW = os.getenv('DB_PW')
DB_URL = os.getenv('DB_URL')

app = FastAPI()

# db예제
uri = f'mongodb+srv://{DB_ID}:{DB_PW}{DB_URL}'

# 1. db client 생성
client = MongoClient(uri)

# 2. 사용하려는 database 특정
db = client.ace_mini

# 3. news라는 collection(table 느낌)으로 연결
news_collection = db.news

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # 허용할 HTTP 메소드
    allow_headers=["*"],  # 모든 헤더를 허용할 경우
    allow_origins=['http://localhost:3000/', 'http://127.0.0.1:3000/']
)

@app.get('/')
async def home(request: Request):
    return { 'message': 'success' }

@app.get('/news/{code}')
async def news(code: str):
    news_list = crawling(code)
    if news_list:
        for news in news_list:
            news_collection.insert_one({
                'reg_user': 'RA',
                'title': news['title'],
                'content': news['content'],
                'author': news['author'],
                'publishedAt': news['publishedAt'],
                'img_url': news['img_url'],
                'news_url': news['news_url']
            })
        return { 'message' : '뉴스 크롤링 성공', 'news': news_list}
    else: 
        return { 'message' : '뉴스 못찾음'}