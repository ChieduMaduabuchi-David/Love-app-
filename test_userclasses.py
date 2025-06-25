import pytest
import datetime
import json
from Userclasses import height, Sex, User, Desire # Assuming Userclasses.py is in the same directory

# --- Test for height class ---
def test_height_init():
    """Test height initialization and unit conversion."""
    h = height(170)
    assert h.cm == 170
    assert f"{h.feet:.2f}" == f"{170 * 0.0328084:.2f}"

def test_height_repr():
    """Test height string representation."""
    h = height(175.5)
    assert repr(h) == "175.5 cm (5.76 ft)"

def test_height_arithmetic():
    """Test arithmetic operations for height."""
    h1 = height(100)
    assert h1 + 20 == 120
    assert 20 + h1 == 120
    assert h1 - 10 == 90
    assert 110 - h1 == 10 # rsub


# --- Test for Sex class ---
def test_sex_init_valid():
    """Test Sex class with valid inputs."""
    s_m1 = Sex("MALE")
    assert s_m1.value == "MALE"
    s_m2 = Sex("m")
    assert s_m2.value == "MALE"

    s_f1 = Sex("FEMALE")
    assert s_f1.value == "FEMALE"
    s_f2 = Sex("f")
    assert s_f2.value == "FEMALE"

def test_sex_init_invalid():
    """Test Sex class with invalid input, expecting ValueError."""
    with pytest.raises(ValueError, match="Only Accepts Male or Female"):
        Sex("OTHER")
    with pytest.raises(ValueError, match="Only Accepts Male or Female"):
        Sex("")

def test_sex_str_repr():
    """Test Sex string representation."""
    s = Sex("M")
    assert str(s) == "MALE"
    assert repr(s) == "Sex('MALE')"

def test_sex_flip():
    """Test the flip method of Sex class."""
    male_sex = Sex("MALE")
    assert male_sex.flip() == "FEMALE"

    female_sex = Sex("FEMALE")
    assert female_sex.flip() == "MALE"


# --- Test for User class ---
# Helper for creating a User instance
def create_test_user_data(user_id=1, username="testuser", birth_year=1990):
    return {
        "id": user_id,
        "name": "Test User",
        "username": username,
        "birthdate": datetime.datetime(birth_year, 1, 1),
        "sex": "MALE",
        "location": "Test City",
        "email": f"{username}@example.com",
        "phone": "123-456-7890",
        "photo": 123,
        "nationality": "Testland",
        "height": height(180),
        "religion": "Agnostic",
        "interest": ["coding", "reading"],
        "intro": "Hello, I am a test user."
    }

def test_user_init():
    """Test User class initialization."""
    user_data = create_test_user_data()
    user = User(**user_data)

    assert user._id == user_data["id"]
    assert user.name == user_data["name"]
    assert user.u_name == user_data["username"]
    assert user.email == user_data["email"]
    assert user.phone_number == user_data["phone"]
    assert user._birthdate == user_data["birthdate"]
    assert user.photo == user_data["photo"]
    assert user.sex.value == "MALE"
    assert user.location == user_data["location"]
    assert user.nationality == user_data["nationality"]
    assert user.height.cm == user_data["height"].cm
    assert user.religion == user_data["religion"]
    assert user.interest == user_data["interest"]
    assert user.intro == user_data["intro"]
    assert user.desire is None # Should be None initially

def test_user_age_calculation(mocker):
    """Test age calculation for User class."""
    # Mock datetime.datetime.now for consistent testing
    mocker.patch('datetime.datetime')
    datetime.datetime.now.return_value = datetime.datetime(2025, 6, 25)
    mocker.patch('pytz.utc.localize', side_effect=lambda x: x) # Mock localize to return same datetime

    user_data = create_test_user_data(birth_year=1990)
    user = User(**user_data)
    assert user.age() == 35 # 2025 - 1990

    # Test age with birthdate later in the year
    user_data_later = create_test_user_data(birth_year=1990)
    user_data_later["birthdate"] = datetime.datetime(1990, 10, 1) # Oct 1st
    user_later = User(**user_data_later)
    assert user_later.age() == 34 # Should be 34 as birthday hasn't passed in 2025

def test_user_default_desire():
    """Test default_desire method for User class."""
    user_data = create_test_user_data()
    user_data["height"] = height(170) # Set a height for calculation
    user = User(**user_data)
    user.default_desire()

    assert isinstance(user.desire, Desire)
    assert user.desire.age == user.age()
    assert user.desire.sex == "FEMALE" # Male user flips to Female
    assert user.desire.location == user.location
    assert user.desire.nationality == user.nationality
    assert user.desire.height == user.height.cm - 11.43 # Male height adjustment
    assert user.desire.intro == user.intro
    assert user.desire.interest == user.interest

    # Test female user height adjustment
    user_data_female = create_test_user_data(sex="FEMALE")
    user_data_female["height"] = height(160)
    user_female = User(**user_data_female)
    user_female.default_desire()
    assert user_female.desire.sex == "MALE" # Female user flips to Male
    assert user_female.desire.height == 21 + user_female.height.cm # Female height adjustment

def test_user_to_json_from_json():
    """Test to_json and from_json methods for User class."""
    user_data = create_test_user_data()
    user_data["birthdate"] = datetime.datetime(1990, 1, 1, 10, 30, 0) # Ensure specific time for string conversion
    user = User(**user_data)

    json_str = user.to_json()
    assert isinstance(json_str, str)
    loaded_user = User.from_json(json_str)

    assert loaded_user._id == user._id
    assert loaded_user.u_name == user.u_name
    assert loaded_user._birthdate == user._birthdate
    assert loaded_user.sex.value == user.sex.value
    assert loaded_user.height.cm == user.height.cm

def test_user_from_json_invalid_data():
    """Test from_json with invalid JSON data."""
    invalid_json = '{"id": 1, "name": "Bad User", "birthdate": "not-a-date"}'
    with pytest.raises(ValueError):
        User.from_json(invalid_json)

    invalid_json_missing_key = '{"id": 1, "name": "Missing Data"}'
    with pytest.raises(TypeError): # Expect TypeError due to missing required arguments
        User.from_json(invalid_json_missing_key)

