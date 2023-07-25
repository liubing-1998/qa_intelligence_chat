import sys

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer
import pydantic
import uvicorn
from config import *
from models.request_model import *
from models.response_model import *

# 创建FastAPI实例
app = FastAPI()

# 加载ChatGPT模型和tokenizer
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL, trust_remote_code=True)
model = AutoModel.from_pretrained(LLM_MODEL, trust_remote_code=True).half().cuda()
model = model.eval()

@app.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    input_text = request.message
    print(input_text)

    response, history = model.chat(tokenizer, input_text, history=[])

    return ChatResponse(reply=response)


@app.post("/llmChat")
def llmChat(request: ChatRequest) -> LLMChatResponse:
    input_text = request.message
    print(input_text)

    response, history = model.chat(tokenizer, input_text, history=[])
    print(response)
    print(history)
    # 这里面history应该怎么存储处理，怎么带入model.chat？
    return LLMChatResponse(response=response, history=history)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


# 启动bert
# bert-serving-start -model_dir E:\LLM\bertsearch-master\chinese_L-12_H-768_A-12 -num_worker=1
