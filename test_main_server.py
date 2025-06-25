import pytest
import socket
import json
import threading
import time
from unittest.mock import MagicMock, patch

# Assuming Main.py, Database.py, and Userclasses.py are in the same directory
from Main import init_connect, server
from Userclasses import User, Sex, height
from Database import register_user, verify_user # Import actual functions for side effects

# Fixture to mock the socket server and client for isolated testing of init_connect
@pytest.fixture
def mock_sockets(mocker):
    """Mocks socket.socket methods and provides mock client/server sockets."""
    mock_server_socket = mocker.MagicMock(spec=socket.socket)
    mock_client_socket = mocker.MagicMock(spec=socket.socket)

    # Mock server.accept() to return our mock client socket
    # This will simulate a client connecting to the server
    mock_server_socket.accept.return_value = (mock_client_socket, ("127.0.0.1", 12345))

    # Patch socket.socket itself to return our mock server socket when Main.py creates it
    mocker.patch('socket.socket', return_value=mock_server_socket)

    # Patch the server.bind and server.listen to do nothing for tests
    mocker.patch.object(server, 'bind')
    mocker.patch.object(server, 'listen')

    yield mock_client_socket, mock_server_socket

# Fixture to clean up the test database after each test
@pytest.fixture(autouse=True)
def clean_db_for_main_tests():
    """Ensures a clean auth.db and userVector_DB for Main.py tests."""
    db_name = 'auth.db'
    vector_db_path = './userVector_DB'

    # Remove existing database files for a clean slate
    if os.path.exists(db_name):
        os.remove(db_name)
    if os.path.exists(vector_db_path):
        import shutil
        shutil.rmtree(vector_db_path)

    # Re-initialize the database connection and tables for the test
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

    # Patch sqlite3.connect to use the test database
    with patch('Database.sqlite3.connect', return_value=sqlite3.connect(db_name)):
        yield

    # Teardown: remove the test database files
    if os.path.exists(db_name):
        os.remove(db_name)
    if os.path.exists(vector_db_path):
        import shutil
        shutil.rmtree(vector_db_path)

# Helper function to create a test user object (same as in test_userclasses.py)
def create_test_user_for_main(user_id=1, username="testuser", sex="MALE"):
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
        nationality="Testland",
        height=height(170),
        religion="Agnostic",
        interest=["coding", "reading"],
        intro="Hello, I am a test user."
    )

# --- Test for init_connect (Signup path) ---
def test_init_connect_signup_success(mock_sockets, mocker):
    """Test init_connect handles successful user signup."""
    client_socket, _ = mock_sockets

    test_user_data = create_test_user_for_main(username="signup_user", user_id=None)
    test_password = "signup_password"

    # Mock client_socket.recv calls
    client_socket.recv.side_effect = [
        "True".encode('utf-8'),  # User wants to sign up
        json.dumps({"Username": "signup_user", "password": test_password}).encode('utf-8'), # Login details
        test_user_data.to_json().encode('utf-8') # User profile data
    ]
    # Mock client_socket.send to record responses
    client_socket.send.side_effect = lambda x: print(f"Sent: {x.decode('utf-8')}")

    # Call the function in a thread as it's designed to be run concurrently
    thread = threading.Thread(target=init_connect, args=(client_socket, ("127.0.0.1", 54321)))
    thread.start()
    thread.join(timeout=2) # Give it some time to complete

    # Verify initial 'Login' message was sent
    client_socket.send.assert_any_call('Login'.encode('utf-8'))

    # Verify response message
    # Due to side_effect being a generator, we need to check the call history
    sent_messages = [call_arg[0].decode('utf-8') for call_arg in client_socket.send.call_args_list]
    assert "User registered and profile saved!" in sent_messages

    # Verify user was actually registered in the DB
    # We use the actual verify_user here to check DB state
    assert verify_user("signup_user", test_password) > 0


def test_init_connect_signup_duplicate_username(mock_sockets, mocker):
    """Test init_connect handles duplicate username during signup."""
    client_socket, _ = mock_sockets

    test_user_data = create_test_user_for_main(username="dup_user", user_id=None)
    test_password = "dup_password"

    # Register the user once beforehand to create the duplicate scenario
    register_user(test_user_data, test_password)

    # Mock client_socket.recv calls for the second signup attempt
    client_socket.recv.side_effect = [
        "True".encode('utf-8'),
        json.dumps({"Username": "dup_user", "password": test_password}).encode('utf-8'),
        test_user_data.to_json().encode('utf-8')
    ]
    client_socket.send.side_effect = lambda x: print(f"Sent: {x.decode('utf-8')}")

    thread = threading.Thread(target=init_connect, args=(client_socket, ("127.0.0.1", 54322)))
    thread.start()
    thread.join(timeout=2)

    sent_messages = [call_arg[0].decode('utf-8') for call_arg in client_socket.send.call_args_list]
    assert "Username already taken." in sent_messages


def test_init_connect_signup_bad_user_data(mock_sockets, mocker):
    """Test init_connect handles bad user data during signup."""
    client_socket, _ = mock_sockets

    # Simulate bad JSON for user profile
    bad_user_json = "not a valid json string"
    test_signup_details = {"Username": "bad_data_user", "password": "pass"}

    client_socket.recv.side_effect = [
        "True".encode('utf-8'),
        json.dumps(test_signup_details).encode('utf-8'),
        bad_user_json.encode('utf-8') # Malformed user data
    ]
    client_socket.send.side_effect = lambda x: print(f"Sent: {x.decode('utf-8')}")


    thread = threading.Thread(target=init_connect, args=(client_socket, ("127.0.0.1", 54323)))
    thread.start()
    thread.join(timeout=2)

    sent_messages = [call_arg[0].decode('utf-8') for call_arg in client_socket.send.call_args_list]
    assert "ERORR: bad data" in sent_messages


# --- Test for init_connect (Login path) ---
def test_init_connect_login_success(mock_sockets, mocker):
    """Test init_connect handles successful user login."""
    client_socket, _ = mock_sockets

    test_username = "login_user"
    test_password = "login_password"

    # Register the user first so they can log in
    test_user_data = create_test_user_for_main(username=test_username, user_id=None)
    register_user(test_user_data, test_password)

    # Mock client_socket.recv calls
    client_socket.recv.side_effect = [
        "False".encode('utf-8'), # User wants to login
        json.dumps({"Username": test_username, "password": test_password}).encode('utf-8') # Login details
    ]
    client_socket.send.side_effect = lambda x: print(f"Sent: {x.decode('utf-8')}")

    # Patch activate_user to avoid implementing its logic for this test
    mocker.patch('Main.activate_user')

    thread = threading.Thread(target=init_connect, args=(client_socket, ("127.0.0.1", 54324)))
    thread.start()
    thread.join(timeout=2)

    client_socket.send.assert_any_call('Login'.encode('utf-8'))
    sent_messages = [call_arg[0].decode('utf-8') for call_arg in client_socket.send.call_args_list]
    assert "Logged in" in sent_messages
    Main.activate_user.assert_called_once()


def test_init_connect_login_user_not_found(mock_sockets, mocker):
    """Test init_connect handles login for a non-existent user."""
    client_socket, _ = mock_sockets

    test_username = "non_existent_user"
    test_password = "any_password"

    client_socket.recv.side_effect = [
        "False".encode('utf-8'),
        json.dumps({"Username": test_username, "password": test_password}).encode('utf-8')
    ]
    client_socket.send.side_effect = lambda x: print(f"Sent: {x.decode('utf-8')}")

    mocker.patch('Main.activate_user')

    thread = threading.Thread(target=init_connect, args=(client_socket, ("127.0.0.1", 54325)))
    thread.start()
    thread.join(timeout=2)

    sent_messages = [call_arg[0].decode('utf-8') for call_arg in client_socket.send.call_args_list]
    assert "user not found" in sent_messages
    Main.activate_user.assert_not_called()


def test_init_connect_login_wrong_password(mock_sockets, mocker):
    """Test init_connect handles login with incorrect password."""
    client_socket, _ = mock_sockets

    test_username = "wrong_pass_user"
    correct_password = "correct_password"
    wrong_password = "incorrect_password"

    test_user_data = create_test_user_for_main(username=test_username, user_id=None)
    register_user(test_user_data, correct_password)

    client_socket.recv.side_effect = [
        "False".encode('utf-8'),
        json.dumps({"Username": test_username, "password": wrong_password}).encode('utf-8')
    ]
    client_socket.send.side_effect = lambda x: print(f"Sent: {x.decode('utf-8')}")

    mocker.patch('Main.activate_user')

    thread = threading.Thread(target=init_connect, args=(client_socket, ("127.0.0.1", 54326)))
    thread.start()
    thread.join(timeout=2)

    sent_messages = [call_arg[0].decode('utf-8') for call_arg in client_socket.send.call_args_list]
    assert "wrong password" in sent_messages
    Main.activate_user.assert_not_called()


