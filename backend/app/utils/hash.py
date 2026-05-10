"""
Password hashing utilities using bcrypt.

Uses bcrypt directly instead of passlib to avoid compatibility issues
with bcrypt >= 4.1.
"""

import bcrypt


def hash_password(password: str) -> str:
    """Return bcrypt hash of the given plaintext password."""
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )
