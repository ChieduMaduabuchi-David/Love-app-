import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# use local sentence-transformers model
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")



def embed(User):
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="users", embedding_function=embedding_fn)
    collection.add(
        documents=[User.text],
        metadatas=[{"id": User.id, "name": User.name}],
        ids=[User.id]
    )

def search(User):
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="users", embedding_function=embedding_fn)
    results = collection.query(
        query_texts=["Looking for someone who likes music and books."],
        n_results=5
    )


