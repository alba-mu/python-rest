import jwt
from argon2 import PasswordHasher
from dataclasses import dataclass
from datetime import timedelta, datetime, timezone

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@dataclass
class User:
    id: str
    password: str
    name: str | None = None
    disabled: bool | None = None

    def __post_init__(self):
        self.password = PasswordHasher().hash(self.password)

    def verify_password(self, plain_password):
        try:
            return PasswordHasher().verify(self.password, plain_password)
        except Exception:
            return False


db: dict[str, User] = {}


def add_user(user: User):
    if user.id in db:
        return False
    db[user.id] = user
    return True


def get_user(id: str):
    return db.get(id)


def authenticate(user: str, password: str):
    user = db.get(user)
    if not user:
        return False
    try:
        user.verify_password(password)
        return True
    except Exception:
        return False


def token_create(user: str, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data = {"sub": user, "exp": expire}
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def token_user(token: str) -> str | None:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = payload.get("sub")
    if user is None:
        return None
    else:
        return db.get(user)
