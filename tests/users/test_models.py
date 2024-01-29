import pytest


def test_user_str(base_user):
    """test cutom user model str representation"""
    assert base_user.__str__() == f"{base_user.username}"
    
def test_user_full_name(base_user):
    """test that user models get_full_name method works"""
    full_name = f"{base_user.first_name.title()} {base_user.last_name.title()}"
    assert base_user.get_full_name == full_name

def test_user_short_name(base_user):
    """test that user models get_short_name method works"""
    assert base_user.get_short_name() == f"{base_user.username}"

def test_base_user_email_is_normalized(base_user):
    """test that new users email is normalized"""
    email = "TestUser@Gmail.coM"
    assert base_user.email == email.lower()

def test_create_user_with_no_email(user_factory):
    """test that error is raised when new user is created without email"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None)
    assert str(err.value) == "Base User Account: An email is required."

def test_create_user_with_no_username(user_factory):
    """test that error is raised when new user is created without username"""
    with pytest.raises(ValueError) as err:
        user_factory.create(username=None)
    assert str(err.value) == "Username must be provided."

def test_create_user_with_no_first_name(user_factory):
    """test that error is raised when new users created without first name"""
    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None)
    assert str(err.value) == "First name must be provided."

def test_create_user_with_no_last_name(user_factory):
    """test that error is raised when new users created without first name"""
    with pytest.raises(ValueError) as err:
        user_factory.create(last_name=None)
    assert str(err.value) == "Last name must be provided."

def test_super_user_email_is_normalized(super_user):
    """test that super_user's email is normalized"""
    email= "Admin@Gmail.Com"
    assert super_user.email == email.lower()

def test_super_user_is_not_staff(user_factory):
    """Test that an error is raised when an admin user has is_staff set to false"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_staff=False, is_superuser=True)
    assert str(err.value) == "Superuser must have is_staff=True"

def test_super_user_is_not_superuser(user_factory):
    """Test that an error is raised when an admin user has is_superuser set to false"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=False, is_staff=True)
    assert str(err.value) == "Superuser must have is_superuser=True"

def test_super_user_is_not_active(user_factory):
    """Test that an error is raised when an admin user has is_active set to false"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, is_staff=True, is_active=False)
    assert str(err.value) == "Superuser must have is_active=True"

def test_create_super_user_with_no_email(user_factory):
    """Test creating a superuser without an email address raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "Admin Account: An email address is required."

def test_create_super_user_with_no_password(user_factory):
    """Test that an error is raised when an admin user is created without password"""
    with pytest.raises(ValueError) as err:
        user_factory.create(password=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "Superuser must have password"

def test_user_has_valid_email_address(user_factory):
    """Test that an error is raised when a user has no valid email"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email="testuser.gmail.com")
    assert str(err.value) == "Valid email address must be provided."
