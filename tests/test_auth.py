import pytest
import jwt

from app.services.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)


def test_hash_password_does_not_return_plaintext():
    plain = "hunter2"
    hashed = hash_password(plain)
    assert hashed != plain
    assert hashed.startswith("$2b$")  # bcrypt marker


def test_verify_password_accepts_correct_password():
    hashed = hash_password("hunter2")
    assert verify_password("hunter2", hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = hash_password("hunter2")
    assert verify_password("wrong-password", hashed) is False


def test_jwt_round_trip_returns_same_user_id():
    token = create_access_token(user_id=42)
    assert isinstance(token, str)
    assert decode_token(token) == 42


def test_decode_token_rejects_tampered_token():
    token = create_access_token(user_id=1)
    # Flip the last character — signature should no longer match.
    tampered = token[:-1] + ("A" if token[-1] != "A" else "B")
    with pytest.raises(jwt.InvalidTokenError):
        decode_token(tampered)
