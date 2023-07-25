import os

# 是否启用 swagger 文档
ENABLE_DOC = os.getenv("ENABLE_DOC", True)

# 配置Elasticsearch信息
# 返回最相似的索引记录数量
SEARCH_SIZE = 5
ELASTICSEARCH_USERNAME = os.getenv("ELASTICSEARCH_USERNAME", "elastic")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD", "WdgfOyS=G=nRz1wT+LqJ")
# index名
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "test_qa")
# ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "jobsearch")
# index mapping 文件名
ELASTICSEARCH_INDEX_FILE = os.getenv("ELASTICSEARCH_INDEX_FILE", "test_index.json")

# 配置大语言模型参数
# 模型参数文件路径
LLM_MODEL = "THUDM\chatglm2-6b-int4"
# 基于上下文的prompt模版，请务必保留"{question}"和"{context}"
PROMPT_TEMPLATE_1 = """已知信息：
{context} 

根据上述已知信息，简洁和专业的来回答用户的问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题” 或 “没有提供足够的相关信息”，不允许在答案中添加编造成分，答案请使用中文。 问题是：{question}"""
PROMPT_TEMPLATE_2 = """已知信息：
{context} 

根据上述已知信息，简洁和专业的来回答用户的问题。如果无法从中得到答案，请总结与问题相关的已知信息，不允许在答案中添加编造成分，答案请使用中文。 问题是：{question}"""

