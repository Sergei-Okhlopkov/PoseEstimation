from argon2 import PasswordHasher

hasher = PasswordHasher()


def get_hash(password) -> str:
    return hasher.hash(password)


def verify_password(password, hashed_password):
    return hasher.verify(hashed_password, password)
