
# STEP 1. import modules
from transformers import pipeline
from transformers import AutoTokenizer


# STEP 2. create inference instance (인퍼런스(추론)할 객체 만들기)
# classifier = pipeline("sentiment-analysis", model="snunlp/KR-FinBert-SC")
#                             # task name             # model ; huggingface 홈페이지에서 조회가능
classifier = pipeline("sentiment-analysis", model="stevhliu/my_awesome_model")


#STEP 3. prepare input data
text = "I don't love you"

# STEP 4. inference 추론
result = classifier(text)

#STEP 4-1. preprocessing (data->tensor(blob))   
#STEP 4-2. inference (tensor(blob) -> logit)
#STEP 4-3. postprocessing(logit -> data)

#STEP 5. visualize
print(result)