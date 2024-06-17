# API key 저장을 위한 os 라이브러리 호출
import os

# openai API 키 저장
# os.environ['OPENAI_API_KEY'] = 'open api key'

from langchain_community.chat_models import ChatOpenAI

# 모델 초기화
chatgpt = ChatOpenAI(model_name='gpt-3.5-turbo')

# 예측 수행
response = chatgpt.invoke("Why is Python the most popular language? Answer in Korean.")
print(response)


### 테스트를 수행하려했으나 Open API의 유료화로 인해 현재 불가능