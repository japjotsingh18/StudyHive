"""Maintained password hashing and cryptographically random session primitives."""

import hashlib
import secrets

from pwdlib import PasswordHash

from studyhive.auth.domain import SessionCredential


class PasswordHasher:
    """Argon2 password adapter backed by pwdlib's maintained recommendation."""

    def __init__(self) -> None:
        self._password_hash = PasswordHash.recommended()
        self._dummy_hash = self._password_hash.hash("studyhive-dummy-password-verification")

    def hash(self, password: str) -> str:
        """Hash a password using the configured adaptive algorithm."""

        return self._password_hash.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        """Verify a password without exposing provider exceptions."""

        return self._password_hash.verify(password, password_hash)

    def verify_dummy(self, password: str) -> None:
        """Spend comparable work for unknown identifiers to reduce timing disclosure."""

        self._password_hash.verify(password, self._dummy_hash)


class SessionTokenFactory:
    """Create opaque browser secrets while storing only SHA-256 lookup digests."""

    @staticmethod
    def digest(secret: str) -> str:
        """Return the fixed-width digest stored by the session repository."""

        return hashlib.sha256(secret.encode("utf-8")).hexdigest()

    def issue(self) -> SessionCredential:
        """Issue independent session and CSRF secrets."""

        token = secrets.token_urlsafe(48)
        csrf_token = secrets.token_urlsafe(32)
        return SessionCredential(
            token=token,
            token_digest=self.digest(token),
            csrf_token=csrf_token,
            csrf_digest=self.digest(csrf_token),
        )
