from datetime import datetime, timedelta, timezone

import jwt

from pwdlib import PasswordHash

from app.config import (
    SECRET_KEY,
    ALGORITHM
)


# ==========================================
# PASSWORD HASHING
# ==========================================

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.
    """

    return password_hash.hash(
        password
    )


def verify_password(
    password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plain-text password
    against its hashed version.
    """

    try:

        return password_hash.verify(
            password,
            hashed_password
        )

    except Exception:

        return False


# ==========================================
# CREATE ACCESS TOKEN
# ==========================================

def create_access_token(
    user_id: int
) -> str:
    """
    Create a JWT access token for a user.
    """

    expiration_time = (
        datetime.now(timezone.utc)
        + timedelta(hours=24)
    )

    payload = {
        "user_id": user_id,
        "exp": expiration_time
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

def decode_access_token(
    token: str
):
    """
    Decode and validate a JWT access token.

    Returns:
        Payload dictionary if valid.
        None if invalid or expired.
    """

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.ExpiredSignatureError:

        return None

    except jwt.InvalidTokenError:

        return None

    except Exception:

        return None