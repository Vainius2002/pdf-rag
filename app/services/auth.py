from passlib.context import CryptContext
from app.config import JWT_SECRET
import jwt
from datetime import datetime, timedelta, timezone

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain):
    return pwd_context.hash(plain)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# CryptContext = the method we use to select our bcrypt recipe, with which when we call hash or verify. Basically we do this so its easier if needed to switch to f.e. argon2. Then we would just change one line in cryptcontext
# hashing = hashes our passwords so instead of f.e. 'bike2' it gives us a long unreadable string and we cant reverse that. so if db gets leaked, our passwrod is safe. We use this at registration
# verify = takes the password the user typed and the hashed string as well, checks to see if they match and returns true or false. We use this at login by basically matching hashed version of password with inputted passwrod during login.


def create_access_token(user_id):
    expire = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRE_HOURS)
    payload = {
        "sub" : str(user_id),
        "exp" : expire,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

#sub = subject, so basically for which user basically
#exp = expiration of our current time + 24 hours
#jwt.encode requires taking our payload, secret and it spits out encoded token string

def decode_token(token):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return int(payload["sub"])