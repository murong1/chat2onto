import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_community.document_loaders import UnstructuredFileLoader

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
        # print(chunk)

    # Run tasks concurrently
    await asyncio.gather(*tasks)
def split_documents_by_empty_line_and_filter(docs):
    # filtered_splits = []
    raw_splits = docs[0].page_content.split('.\n\n')
    return raw_splits


def traverse_two_levels(root_dir,collection):
    # 遍历一级文件夹
    for root, dirs, files in os.walk(root_dir):
        # 遍历二级文件夹，但不再深入
        for dir in dirs:
            second_level_dir = os.path.join(root, dir)
            for second_root, second_dirs, second_files in os.walk(second_level_dir):
                for file in second_files:
                    file_path = os.path.join(second_root, file)
                    print(f"File: {file_path}")
                    loader = UnstructuredFileLoader(file_path)
                    docs = loader.load()
                    splits = split_documents_by_empty_line_and_filter(docs)
                    # print(splits)
                    asyncio.run(process_chunks_async(splits, collection))
            # 不再深入到更多的子文件夹
        break
def get_collection():
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_base="https://api.oaipro.com/v1",
        api_key="sk-qv7leQ5iQl30aQoKE824D152E70643B59607C8Bf69C4943e",
        model_name="text-embedding-3-large"
    )
    # 文件存储路径
    client = chromadb.PersistentClient(path="./tmp/.chroma")
    collection_name = "tcp"
    collection = client.get_or_create_collection(name=collection_name, embedding_function=openai_ef)
    return collection


collection = get_collection()

traverse_two_levels("text", collection)


