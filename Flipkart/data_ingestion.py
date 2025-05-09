from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
from Flipkart.data_converter import dataconvertor

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")
HF_TOKEN = os.getenv("HF_TOKEN")

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5",
    model_kwargs={"token": HF_TOKEN}
)

def data_ingestion(status):
    vstore = AstraDBVectorStore(
        embedding = embedding_model,
        collection_name="Flipkart1",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE
    )
    storage = status
    
    if storage == None:
        docs = dataconvertor()
        insert_ids = vstore.add_documents(docs)
    else:
        return vstore

    return vstore, insert_ids

if __name__ == "__main__":
    vstore, insert_ids = data_ingestion(None)
    print(f"\n Inserted {len(insert_ids)} documents.")
    results = vstore.similarity_search("Can you give me a laptop list?")
    for res in results:
        print(f"\n {res.page_content} [{res.metadata}]")