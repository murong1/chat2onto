import time
import uuid


import chromadb
from chromadb.utils import embedding_functions
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import asyncio
import uuid

async def add_chunk_async(collection, chunk):
    # Asynchronously add the chunk to the collection
    collection.add(
        documents=chunk,
        ids=[uuid.uuid4().hex],
    )
    # time.sleep(0.011)
async def process_chunks_async(splits, collection):
    # Create a list of tasks to add chunks concurrently
    tasks = []
    for chunk in splits:
        task = add_chunk_async(collection, chunk)
        tasks.append(task)
        print(chunk)

    # Run tasks concurrently
    await asyncio.gather(*tasks)
def split_documents_by_empty_line_and_filter(docs):
    # filtered_splits = []
    raw_splits = docs[0].page_content.split('.\n\n')
    return raw_splits


openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_base="https://api.oaipro.com/v1",
    api_key="sk-qv7leQ5iQl30aQoKE824D152E70643B59607C8Bf69C4943e",
    model_name="text-embedding-3-large"
)

# 文件存储路径
client = chromadb.PersistentClient(path="./tmp/.chroma")
collection_name = "tcp"
# client.delete_collection(collection_name)

collection = client.get_or_create_collection(name=collection_name, embedding_function=openai_ef)

loader = UnstructuredFileLoader('tcp.txt')
docs = loader.load()

splits = split_documents_by_empty_line_and_filter(docs)
asyncio.run(process_chunks_async(splits, collection))

#
# # 获取控制台输入
# while True:
#     print('请输入搜索内容')
#     search_text = input()
#     results = collection.query(
#         query_texts=[search_text],
#         n_results=4,
#     )
#     print('search')
#     print(results)
#     # {'ids': [['doc1', 'doc2']], 'distances': [[0.4450637689775306, 0.4570213244723775]], 'metadatas': [[{'source': 'notion'}, {'source': 'google-docs'}]], 'embeddings': None, 'documents': [['This is document1', 'This is document2']], 'uris': None, 'data': None}
#     # 打印 2 个最相似的结果
#     for i, result in enumerate(results['documents'][0]):
#         print(f"Result {i}: {result}")
#         print(f"Distance: {results['distances'][0][i]}")
#         print(f"Metadata: {results['metadatas'][0][i]}")
#         print(f"ID: {results['ids'][0][i]}")
#         print()



