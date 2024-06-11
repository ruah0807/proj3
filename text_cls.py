
# STEP 1. import modules
from transformers import pipeline
from transformers import AutoTokenizer


# STEP 2. create inference instance (인퍼런스(추론)할 객체 만들기)
# classifier = pipeline("sentiment-analysis", model="maidalun1020/bce-reranker-base_v1 ")
#                             # task name             # model ; huggingface 홈페이지에서 조회가능
classifier = pipeline("sentiment-analysis", model="snunlp/KR-FinBert-SC")


#STEP 3. prepare input data
text = "지디넷코리아LG이노텍은 회사 제도와 관련한 직원들의 다양한 의견을 청취하고 적극 실행하기 위한 소통 경영에 주력한다고 10일 밝혔다LG이노텍의 소통 경영 중심에는 직원 누구나 자유롭게 의견을 개진할 수 있는 소통 창구인 이노 보이스Inno Voice가 있다이노 보이스는 사무직 대표인 주니어 보드가 업무 포털에 개설한 소통 창구다 회사 제도 업무 환경 등에 관한 의견을 자유롭게 공유할 수 있다 제안에 댓글을 달 수 있고 공감도 표시할 수"

# STEP 4. inference 추론
result = classifier(text)

#STEP 4-1. preprocessing (data->tensor(blob))   
#STEP 4-2. inference (tensor(blob) -> logit)
#STEP 4-3. postprocessing(logit -> data)

#STEP 5. visualize
print(result)