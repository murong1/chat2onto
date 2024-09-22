import chromadb
from chromadb.utils import embedding_functions

def getBackgroundText(query):
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_base="https://api.oaipro.com/v1",
        api_key="sk-qv7leQ5iQl30aQoKE824D152E70643B59607C8Bf69C4943e",
        model_name="text-embedding-3-large"
    )
    # 文件存储路径
    client = chromadb.PersistentClient(path="C:/Users/Administrator/PycharmProjects/Chat2onto/vector_stores/tmp/.chroma")
    collection_name = "tcp"
    collection = client.get_or_create_collection(name=collection_name, embedding_function=openai_ef)

    results = collection.query(
        query_texts=[query],
        n_results=4,
    )
    return results['documents']

# test
# print(getBackgroundText(' TCP guarantees the reliable, in-order delivery of a stream of bytes'))








