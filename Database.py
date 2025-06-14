import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# use local sentence-transformers model
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="users", embedding_function=embedding_fn)

def embed(User):

    collection.add(
        documents=[User.text],
        metadatas=[{"id": 1, "name": "Paul"}],
        ids=[User.id]
    )

def search()
    results = collection.query(
        query_texts=["Looking for someone who likes music and books."],
        n_results=5
    )

print(results)
