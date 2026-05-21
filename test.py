from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

password = "test12"

hashed = pwd_context.hash(password)

print(hashed)

print(
    pwd_context.verify("test12", hashed)
)