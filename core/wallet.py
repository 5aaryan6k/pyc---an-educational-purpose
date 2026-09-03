from dataclasses import dataclass

from core.crypto import (
    b64_encode,
    b64_decode,
    decrypt_private_key,
    encrypt_private_key,
    generate_wallet_keys,
    public_key_to_address,
    sign_message,
)


@dataclass
class Wallet:
    address: str
    public_key: str
    encrypted_private_key: str
    encryption_salt: str

    @classmethod
    def create(
        cls,
        password: str,
    ):

        private_key, public_key = (
            generate_wallet_keys()
        )

        address = public_key_to_address(
            public_key
        )

        salt, encrypted_private_key = (
            encrypt_private_key(
                private_key,
                password,
            )
        )

        return cls(
            address=address,
            public_key=b64_encode(
                public_key
            ),
            encrypted_private_key=(
                encrypted_private_key
            ),
            encryption_salt=salt,
        )

    def sign(
        self,
        message: str,
        password: str,
    ) -> str:

        private_key = decrypt_private_key(
            self.encrypted_private_key,
            self.encryption_salt,
            password,
        )

        signature = sign_message(
            private_key,
            message,
        )

        return b64_encode(
            signature
        )

    def get_public_key_bytes(self):
        return b64_decode(
            self.public_key
        )