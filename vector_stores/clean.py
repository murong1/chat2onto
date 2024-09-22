import chromadb
from chromadb.utils import embedding_functions

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_base="https://api.oaipro.com/v1",
        api_key="sk-qv7leQ5iQl30aQoKE824D152E70643B59607C8Bf69C4943e",
        model_name="text-embedding-ada-002"
    )
    # 文件存储路径
client = chromadb.PersistentClient(path="./tmp/.chroma")
collection_name = "tcp"
collection = client.get_or_create_collection(name=collection_name, embedding_function=openai_ef)

# 获取所有文档及其id
all_data = collection.get()

# data = [docid for doc, docid in zip(all_data['documents'],all_data['ids']) if doc[0:2]=='[i']
# if data:
#     collection.delete(data)