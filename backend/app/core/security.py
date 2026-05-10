"""
JWT token creation and verification utilities.
"""

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: int | None = None) -> str:
    """Create a signed JWT access token.

    Args:
        data: Payload to encode (typically {"sub": username}).
        expires_delta: Override expiry in minutes. Defaults to config value (240 min / 4 hrs).

    Returns:
        Encoded JWT string.
    """
    to_encode = data.copy()
    minutes = expires_delta if expires_delta is not None else ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict | None:
    """Decode and verify a JWT token.

    Returns:
        The decoded payload dict, or None if the token is invalid/expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
