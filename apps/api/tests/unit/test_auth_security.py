from studyhive.auth.security import PasswordHasher, SessionTokenFactory


def test_password_hasher_verifies_argon2_hash_without_retaining_password() -> None:
    hasher = PasswordHasher()

    password_hash = hasher.hash("violet orbit correct staple")

    assert password_hash.startswith("$argon2")
    assert "violet orbit correct staple" not in password_hash
    assert hasher.verify("violet orbit correct staple", password_hash)
    assert not hasher.verify("incorrect password", password_hash)


def test_session_token_factory_issues_independent_opaque_secrets_and_digests() -> None:
    factory = SessionTokenFactory()

    first = factory.issue()
    second = factory.issue()

    assert first.token != second.token
    assert first.csrf_token != first.token
    assert first.token_digest == factory.digest(first.token)
    assert first.csrf_digest == factory.digest(first.csrf_token)
    assert first.token not in first.token_digest
