import json
import sys
import requests
from utils.elasticsearchClient import ESClient
import utils.config as config

# 自然语言处理模型client
from bert_serving.client import BertClient
bc = BertClient(output_fmt='list')


# 文本生成向量
def bulk_predict(docs, batch_size=256):
    """Predict bert embeddings."""
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i: i + batch_size]
        embeddings = bc.encode([doc['content'] for doc in batch_docs])
        for emb in embeddings:
            yield emb

def create_document(doc, emb, index_name):
    return {
        '_op_type': 'index',
        '_index': index_name,
        'text': doc['summary'],
        'title': doc['content'],
        'text_vector': emb
    }

class QAService:

    # 建立es链接
    def __init__(self):
        self._esClient = ESClient()

    # es建立索引
    def create_index(self):
        self._esClient.create_index(index_json_name=config.ELASTICSEARCH_INDEX_FILE, index_name=config.ELASTICSEARCH_INDEX)

    # 添加索引


    # 加载数据，调用批量添加索引
    def bulk_add_index(self, docs_data_file_path='../knowledge_content/DianXinDataAll.json'):
        with open(docs_data_file_path, 'r', encoding="UTF-8") as fp:
            docs = json.loads(fp.read())

        with open('../knowledge_content/documents.jsonl', 'w', encoding="UTF-8") as f:
            for doc, emb in zip(docs, bulk_predict(docs)):
                d = create_document(doc, emb, config.ELASTICSEARCH_INDEX)
                f.write(json.dumps(d) + '\n')

        with open('../knowledge_content/documents.jsonl', encoding="UTF-8") as f:
            docs = [json.loads(line) for line in f]

        self._esClient.bulk_add_index(docs)

    # 调用自然语言处理模型，讲query文本转换为向量
    def get_embedding(self, query):
        return bc.encode(query)[0]

    # cosineSimilarity向量相似匹配搜索索引文档
    def searchQA(self, query_vector, limit: int=config.SEARCH_SIZE):
        script_query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'text_vector') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
        knowledges = self._esClient.search_documents(config.ELASTICSEARCH_INDEX, script_query, limit)
        return knowledges

    # 生成prompt
    def generate_prompt(self, query, knowledges):
        print("knowledges==", knowledges)
        context = "\n".join([knowledge['_source']['title'] + "  " + knowledge['_source']['text'] for knowledge in knowledges])
        prompt = config.PROMPT_TEMPLATE_2.replace("{question}", query[0]).replace("{context}", context)
        return prompt

    # 调用大模型，prompt做输入
    def chat_with_api(self, message: str) -> str:
        url = "http://localhost:8000/llmChat"  # 替换为实际的URL
        # 创建请求体
        payload = {"message": message}
        # 发送POST请求
        response = requests.post(url, json=payload)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应JSON
            response_json = response.json()
            reply = response_json["response"]
            history = response_json["history"]
            return reply, history
        else:
            # 处理请求失败的情况
            return "Error: Chat request failed"



if __name__ == '__main__':
    qa = QAService()
    qa.create_index()
    qa.bulk_add_index()
    query = ["营改增"]
    query_vector = qa.get_embedding(query)
    knowledges = qa.searchQA(query_vector)
    print("------------------------------------")
    prompt = qa.generate_prompt(query, knowledges)
    print("------------------------------------")
    print(prompt)
    print()
    reply, history = qa.chat_with_api(prompt)
    print(reply)
    print()
    print(history)


