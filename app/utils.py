from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed(password: str):
    return pwd_context.hash(password)


def verify(attempted_password, usr_password):
    return pwd_context.verify(attempted_password, usr_password)
