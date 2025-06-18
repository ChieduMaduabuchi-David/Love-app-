import chromadb
import sqlite3
import bcrypt
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


# Connect (creates file `auth.db` if not exists)
conn = sqlite3.connect('auth.db')
cursor = conn.cursor()

# Create users table (only once)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
''')
conn.commit()

# embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(
    "./userVector_DB"  # or any path you want
)
collection = client.get_or_create_collection(name="users")

#embedding_function = embedding_fn)
# use local sentence-transformers model


def register_user(user,password):
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (user.u_name, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid  # Get the new user's SQLite ID

        # Save user profile in ChromaDB with description
        user._id = user_id #Have to change it to use a function in user
        embed(user)
        print("User registered and profile saved!")
    except sqlite3.IntegrityError:
        print("Username already taken.")


def verify_user(username, password):
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row is None:
        return 0.0  # User not found

    user_id, stored_hash = row
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        print('problem 1')
        return user_id
    else:
        print('problem 2')
        return 0.1 # Incorrect password


def embed(user):
    collection.add(
        documents=[str(user)],
        metadatas=[{"name": f"{user.name}"}],
        ids=[f"{user._id}"]
    )

def recommend_users(user):

    results = collection.query(
        query_texts = [str(user.desire)],
        n_results=5
    )
    results = results['ids'][0]
    results.remove(str(user._id))
    return results

def user_data(id):
        result = collection.get(ids=[str(id)])


