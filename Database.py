import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from Userclasses import *

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="users")
# use local sentence-transformers model
#embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

#embedding_function = embedding_fn)

def embed(user):
    collection.add(
        documents=[user.text()],
        metadatas=[{"id": f"{user.id}", "name": f"{user.name}"}],
        ids=[f"{user.id}"]
    )

def search(user):
    # print(str(user.desire))

    results = collection.query(
        query_texts= [str(user.desire)],
        n_results=5
    )
    return results


