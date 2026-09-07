from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


# ==============================
# HASH PASSWORD
# ==============================

def hash_password(password):
    return password_hash.hash(password)


# ==============================
# VERIFY PASSWORD
# ==============================

def verify_password(password, hashed_password):
    return password_hash.verify(
        password,
        hashed_password
    )