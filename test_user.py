from user import *

add_user(User("david", "password"))
add_user(User("alice", "password", disabled=True))


def test_user():
    david = User("david", "password")
    assert david.password is not "password"
    assert david.verify_password("password")

def test_db():
    assert get_user("mary") is None

def test_create_token():
    token = token_create("david", expires_delta=timedelta(minutes=15))
    assert token_user(token).id == "david"

def test_authenticate():
    add_user(User("alba", "1234"))
    assert authenticate("alba", "1234")
    assert not authenticate("pere", "1234")
