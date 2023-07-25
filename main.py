from typing import Optional
import uvicorn
import utils.config as config
from fastapi import FastAPI
from services.qa_service import QAService
from models.request_model import *
from models.response_model import *

print(config.ENABLE_DOC)
if config.ENABLE_DOC:
    app = FastAPI()
else:
    app = FastAPI(
        title=None,
        description=None,
        docs_url=None,  # 默认的设置对应着 /docs
        redoc_url=None,  # 默认的设置对应着 /redocs
        openapi_url=None  # 默认的设置对应着 /openapi.json
    )

service = QAService()

@app.post("/main")
def main(request: ChatRequest) -> LLMChatResponse:
    input_text = request.message
    print(input_text)

    qa = QAService()
    # qa.create_index()
    # qa.bulk_add_index()
    query = [input_text]
    query_vector = qa.get_embedding(query)
    knowledges = qa.searchQA(query_vector)
    print("------------------------------------")
    prompt = qa.generate_prompt(query, knowledges)
    print("------------------------------------")
    print("prompt: ")
    print(prompt)
    print()
    response, history = qa.chat_with_api(prompt)
    print("response: ", response)
    print("history: ", history)

    return LLMChatResponse(response=response, history=history)

# @app.on_event("startup")
# async def startup_event():
#     service.create_index()
#     if config.LOAD_DATA:
#         service.loadData()
#     print("startup complete")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run(app="main:app", host="localhost", port=8060)

# 启动bert
# bert-serving-start -model_dir E:\LLM\bertsearch-master\chinese_L-12_H-768_A-12 -num_worker=1

