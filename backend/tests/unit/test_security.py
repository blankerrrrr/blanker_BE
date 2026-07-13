from app.core.security import hash_password, verify_password


def test_hash_password_uses_argon2() -> None:
    password_hash = hash_password("strong-password")

    assert password_hash.startswith("$argon2")
    assert verify_password("strong-password", password_hash)
    assert not verify_password("wrong-password", password_hash)
