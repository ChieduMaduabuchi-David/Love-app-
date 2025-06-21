from itertools import count

import chromadb
import sqlite3
import bcrypt
import time
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
conn.close()

embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(
    "./userVector_DB"  # or any path you want
)
collection = client.get_or_create_collection(name="users",embedding_function=embedding_fn)

#embedding_function = embedding_fn)
# use local sentence-transformers model


def register_user(user,password):
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    count=0
    for attempt in range(5):
        try:
            conn = sqlite3.connect('auth.db')
            cursor = conn.cursor()
            # print(user.u_name)
            # print(user._id)
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (user.u_name, password_hash)
            )
            conn.commit()
            conn.close()
            user_id = cursor.lastrowid  # Get the new user's SQLite ID

            # Save user profile in ChromaDB with description
            user._id = user_id #Have to change it to use a function in user
            try:
                embed(user)
            except PermissionError:
                print(f"Data base discrepancy at {user._id}")

            print(user.name)
            return "User registered and profile saved!"
        except sqlite3.IntegrityError:
            print(200)
            conn.close()
            return "Username already taken."
        except sqlite3.OperationalError as e:
            print(300)
            if "database is locked" in str(e):
                conn.close()
                count +=count
                time.sleep(0.01)  # Wait a bit and retry
            # else:
            #     conn.close()
            #     return "ERROR SAVING !!!!!"
    if count>=4:
        return 'too may ops'
    return 'i knoweth not'


def verify_user(username, password):
    conn = sqlite3.connect('auth.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
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
    if user._id == []:
        raise ValueError("NO ID given")
    else:
        if not collection.get(ids=[str(user._id)])['ids']:
            collection.add(
                documents=[str(user)],
                metadatas=[{"name": f"{user.name}"}],
                ids=[f"{user._id}"]
            )
        else:
            raise PermissionError(f"Cannot register: user {user.u_name} already exists.")

def recommend_users(user):

    results = collection.query(
        query_texts = [str(user.desire)],
        n_results=5
    )
    results = results['ids'][0]
    results.remove(str(user._id))
    return results

def find_user(id):
        result = collection.get(ids=[str(id)])
        return result


