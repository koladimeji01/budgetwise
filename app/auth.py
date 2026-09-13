from pwdlib import PasswordHash
import jwt

from app.config import SECRET_KEY, ALGORITHM


# ==========================================
# PASSWORD HASHING
# ==========================================

password_hash = PasswordHash.recommended()


# ==========================================
# HASH PASSWORD
# ==========================================

def hash_password(password):
    return password_hash.hash(password)


# ==========================================
# VERIFY PASSWORD
# ==========================================

def verify_password(password, hashed_password):
    return password_hash.verify(
        password,
        hashed_password
    )


# ==========================================
# CREATE ACCESS TOKEN
# ==========================================

def create_access_token(user_id):

    payload = {
        "user_id": user_id
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# ==========================================
# DECODE ACCESS TOKEN
# ==========================================

def decode_access_token(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.InvalidTokenError:

        return None 