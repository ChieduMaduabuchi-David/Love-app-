import pytest
import sqlite3
import bcrypt
import os
from unittest.mock import MagicMock, patch
from Userclasses import User, height, Sex # Assuming Userclasses.py is in the same directory
import datetime

# Mock the embedding function and chromadb client to avoid actual DB calls during unit tests
@pytest.fixture(autouse=True)
def mock_chromadb():
    """Mocks chromadb for testing database functions without a real ChromaDB."""
    with patch('Database.chromadb') as mock_chromadb_module:
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_chromadb_module.PersistentClient.return_value = mock_client
        mock_client.get_or_create_collection.return_value = mock_collection

        # Mock the collection methods
        mock_collection.get.return_value = {'ids': []} # Default: user not found
        mock_collection.query.return_value = {'ids': [[]]} # Default: empty results for recommendations

        yield mock_collection # Yield the mock collection for specific assertions

@pytest.fixture
def clean_db():
    """Fixture to set up and tear down a clean auth.db for each test."""
    db_name = 'test_auth.db'
    if os.path.exists(db_name):
        os.remove(db_name)

    # Re-initialize the database connection and tables for the test
    # This part should ideally be in the Database.py setup, but for testing,
    # we replicate it here to ensure a clean state.
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

    # Patch the sqlite3.connect in Database.py to use the test database
    with patch('Database.sqlite3.connect', return_value=sqlite3.connect(db_name)):
        yield db_name # Yield control to the test function

    # Teardown: remove the test database file
    if os.path.exists(db_name):
        os.remove(db_name)

# Helper function to create a test user object
def create_test_user(user_id=None, username="testuser", sex="MALE"):
    if user_id is None:
        user_id = 1 # Default ID if not provided, register_user will set it
    return User(
        id=user_id,
        name="Test Name",
        username=username,
        birthdate=datetime.datetime(1990, 1, 1),
        sex=sex,
        location="Test Location",
        email=f"{username}@example.com",
        phone="1234567890",
        photo=1,
        nationality="Test",
        height=height(170),
        religion="None",
        interest=["test"],
        intro="Test intro"
    )

# Import functions to be tested AFTER the mocks are set up if they load modules at import time
# For this structure, we'll import them inside test functions or rely on the fixture's patch.
# A better approach would be to make Database.py functions accept connection objects.
from Database import register_user, verify_user, embed, recommend_users, find_user


# --- Test for register_user ---
def test_register_user_success(clean_db, mock_chromadb):
    """Test successful user registration."""
    user = create_test_user(username="newuser")
    password = "securepassword"
    response = register_user(user, password)
    assert response == "User registered and profile saved!"

    conn = sqlite3.connect(clean_db)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password_hash FROM users WHERE username = ?", ("newuser",))
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "newuser"
    assert bcrypt.checkpw(password.encode('utf-8'), row[1])

    # Check if embed was called
    mock_chromadb.add.assert_called_once()
    args, _ = mock_chromadb.add.call_args
    assert 'documents' in args[0] and str(user) in args[0]['documents']
    assert 'ids' in args[0] and str(user._id) in args[0]['ids'] # _id should be set by register_user


def test_register_user_duplicate_username(clean_db, mock_chromadb):
    """Test registration with a duplicate username."""
    user1 = create_test_user(username="duplicate")
    user2 = create_test_user(username="duplicate")
    password = "password123"

    register_user(user1, password) # First registration should succeed
    response = register_user(user2, password) # Second registration should fail

    assert response == "Username already taken."
    # Ensure embed was only called once for the first successful registration
    mock_chromadb.add.assert_called_once()

# --- Test for verify_user ---
def test_verify_user_success(clean_db, mock_chromadb):
    """Test successful user verification."""
    user = create_test_user(username="validuser")
    password = "validpassword"
    register_user(user, password) # Register the user first

    result = verify_user("validuser", password)
    assert isinstance(result, int) # Should return the user_id (an integer)
    assert result > 0 # User ID should be positive

def test_verify_user_incorrect_password(clean_db, mock_chromadb):
    """Test user verification with an incorrect password."""
    user = create_test_user(username="userpass")
    register_user(user, "correctpassword")

    result = verify_user("userpass", "wrongpassword")
    assert result == 0.1 # Incorrect password

def test_verify_user_not_found(clean_db):
    """Test user verification for a non-existent user."""
    result = verify_user("nonexistent", "anypassword")
    assert result == 0.0 # User not found


# --- Test for embed ---
def test_embed_success(mock_chromadb):
    """Test embed function adds user to ChromaDB."""
    user = create_test_user(user_id=1, username="embedtest")
    user._id = 1 # Manually set ID for testing embed function directly
    embed(user)
    mock_chromadb.add.assert_called_once_with(
        documents=[str(user)],
        metadatas=[{"name": "Test Name"}],
        ids=["1"]
    )

def test_embed_no_id_raises_error():
    """Test embed raises ValueError if user._id is not set."""
    user = create_test_user(user_id=[]) # Simulate no ID
    with pytest.raises(ValueError, match="NO ID given"):
        embed(user)

def test_embed_user_already_exists(mock_chromadb):
    """Test embed raises PermissionError if user already exists in ChromaDB."""
    user = create_test_user(user_id=2, username="existinguser")
    user._id = 2 # Manually set ID
    mock_chromadb.get.return_value = {'ids': ['2']} # Simulate user already exists

    with pytest.raises(PermissionError, match=f"Cannot register: user {user.u_name} already exists."):
        embed(user)
    # Ensure add was NOT called
    mock_chromadb.add.assert_not_called()


# --- Test for recommend_users ---
def test_recommend_users_success(mock_chromadb):
    """Test recommend_users returns a list of recommended user IDs."""
    user = create_test_user(user_id=10, username="recommender")
    user.default_desire() # Ensure desire is set for querying

    # Mock ChromaDB's query result
    mock_chromadb.query.return_value = {
        'ids': [['1', '2', '3', '10', '4']], # Simulate recommendations, including self
        'distances': [[0.1, 0.2, 0.3, 0.0, 0.4]],
        'embeddings': [[]], 'metadatas': [[{}, {}, {}, {}, {}]]
    }

    recommendations = recommend_users(user)
    assert isinstance(recommendations, list)
    assert '10' not in recommendations # Self-ID should be removed
    assert set(recommendations) == {'1', '2', '3', '4'}

    mock_chromadb.query.assert_called_once()
    args, kwargs = mock_chromadb.query.call_args
    assert kwargs['query_texts'] == [str(user.desire)]
    assert kwargs['n_results'] == 5

def test_recommend_users_no_recommendations(mock_chromadb):
    """Test recommend_users returns empty list if no recommendations."""
    user = create_test_user(user_id=100, username="norec")
    user.default_desire()

    # Mock ChromaDB to return empty results
    mock_chromadb.query.return_value = {'ids': [[]], 'distances': [[]], 'embeddings': [[]], 'metadatas': [[]]}

    recommendations = recommend_users(user)
    assert recommendations == []

# --- Test for find_user ---
def test_find_user_success(mock_chromadb):
    """Test find_user retrieves user from ChromaDB."""
    user_id_to_find = "5"
    mock_chromadb.get.return_value = {'ids': [user_id_to_find], 'documents': ["User data for 5"], 'metadatas': [{}]}

    result = find_user(user_id_to_find)
    assert result['ids'] == [user_id_to_find]
    mock_chromadb.get.assert_called_once_with(ids=[user_id_to_find])

def test_find_user_not_found(mock_chromadb):
    """Test find_user returns empty result if user not found."""
    user_id_to_find = "999"
    mock_chromadb.get.return_value = {'ids': [], 'documents': [], 'metadatas': []}

    result = find_user(user_id_to_find)
    assert result['ids'] == []
    mock_chromadb.get.assert_called_once_with(ids=[user_id_to_find])

