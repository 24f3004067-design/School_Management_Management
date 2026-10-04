import os
import bcrypt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jose import jwt


load_dotenv()


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


# Hash password
def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()
    ).decode("utf-8")


# Check password
def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# Create JWT token
def create_access_token(user_id: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    data = {"sub": user_id,"exp": expire}
    return jwt.encode(data, JWT_SECRET_KEY,algorithm=JWT_ALGORITHM)


# Read JWT token
def decode_access_token(token: str):
    try:
        data = jwt.decode(token,JWT_SECRET_KEY,algorithms=[JWT_ALGORITHM])
        return data["sub"]
    
    except Exception:
        raise ValueError("Invalid or expired token")