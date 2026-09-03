import base64
import hashlib
import hmac
import os

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# =========================================================
# Base64
# =========================================================

def b64_encode(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def b64_decode(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


# =========================================================
# Password hashing
# =========================================================

def hash_password(password: str):
    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        310_000,
    )

    return (
        b64_encode(salt),
        b64_encode(password_hash),
    )


def verify_password(
    password: str,
    salt_b64: str,
    stored_hash_b64: str,
) -> bool:

    salt = b64_decode(salt_b64)
    stored_hash = b64_decode(stored_hash_b64)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        310_000,
    )

    return hmac.compare_digest(
        password_hash,
        stored_hash,
    )


# =========================================================
# Key derivation
# =========================================================

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive a 256-bit encryption key from the user's password.
    """

    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        310_000,
        dklen=32,
    )


# =========================================================
# Private-key encryption
# =========================================================

def encrypt_private_key(
    private_key: bytes,
    password: str,
) -> tuple[str, str]:

    salt = os.urandom(16)

    key = derive_key(
        password,
        salt,
    )

    nonce = os.urandom(12)

    aes = AESGCM(key)

    encrypted = aes.encrypt(
        nonce,
        private_key,
        None,
    )

    payload = nonce + encrypted

    return (
        b64_encode(salt),
        b64_encode(payload),
    )


def decrypt_private_key(
    encrypted_b64: str,
    salt_b64: str,
    password: str,
) -> bytes:

    salt = b64_decode(salt_b64)

    payload = b64_decode(
        encrypted_b64
    )

    nonce = payload[:12]
    encrypted = payload[12:]

    key = derive_key(
        password,
        salt,
    )

    aes = AESGCM(key)

    return aes.decrypt(
        nonce,
        encrypted,
        None,
    )


# =========================================================
# Wallet keys
# =========================================================

def generate_wallet_keys():

    private_key = (
        Ed25519PrivateKey.generate()
    )

    public_key = (
        private_key.public_key()
    )

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    return (
        private_bytes,
        public_bytes,
    )


# =========================================================
# Wallet address
# =========================================================

def public_key_to_address(
    public_key: bytes,
) -> str:

    digest = hashlib.sha256(
        public_key
    ).hexdigest()

    return "PYC" + digest[:40]


# =========================================================
# Signing
# =========================================================

def sign_message(
    private_key_bytes: bytes,
    message: str,
) -> bytes:

    private_key = (
        Ed25519PrivateKey.from_private_bytes(
            private_key_bytes
        )
    )

    return private_key.sign(
        message.encode("utf-8")
    )


# =========================================================
# Signature verification
# =========================================================

def verify_signature(
    public_key_bytes: bytes,
    signature: bytes,
    message: str,
) -> bool:

    try:

        public_key = (
            Ed25519PublicKey.from_public_bytes(
                public_key_bytes
            )
        )

        public_key.verify(
            signature,
            message.encode("utf-8"),
        )

        return True

    except (
        InvalidSignature,
        ValueError,
    ):
        return False