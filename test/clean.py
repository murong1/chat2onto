import chromadb
from chromadb.utils import embedding_functions

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_base="https://api.oaipro.com/v1",
        api_key="sk-qv7leQ5iQl30aQoKE824D152E70643B59607C8Bf69C4943e",
        model_name="text-embedding-3-large"
    )
    # 文件存储路径
client = chromadb.PersistentClient(path="./tmp/.chroma")
collection_name = "tcp"
collection = client.get_or_create_collection(name=collection_name, embedding_function=openai_ef)

# 获取所有文档及其id
all_data = collection.get()

# 打印筛选后的文档
print(all_data)
