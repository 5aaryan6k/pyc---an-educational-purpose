import hashlib
import json
import time
import uuid
from dataclasses import dataclass, asdict
from decimal import Decimal, InvalidOperation

from core.crypto import (
    b64_decode,
    public_key_to_address,
    verify_signature,
)


@dataclass
class Transaction:

    transaction_id: str

    sender: str

    receiver: str

    amount: str

    timestamp: float

    public_key: str

    signature: str

    invoice_id: str | None = None

    def unsigned_data(self):

        return {
            "transaction_id": self.transaction_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "invoice_id": self.invoice_id,
        }

    def signing_payload(self):

        return json.dumps(
            self.unsigned_data(),
            sort_keys=True,
            separators=(",", ":"),
        )

    def transaction_hash(self):

        return hashlib.sha256(
            self.signing_payload().encode()
        ).hexdigest()

    def to_dict(self):

        return asdict(self)

    @classmethod
    def create(
        cls,
        sender,
        receiver,
        amount,
        wallet,
        password,
        invoice_id=None,
    ):

        amount = Decimal(
            str(amount)
        ).quantize(
            Decimal("0.01")
        )

        transaction = cls(
            transaction_id=(
                "TX-"
                + uuid.uuid4().hex[:16].upper()
            ),
            sender=sender,
            receiver=receiver,
            amount=format(
                amount,
                "f",
            ),
            timestamp=time.time(),
            public_key=wallet.public_key,
            signature="",
            invoice_id=invoice_id,
        )

        transaction.signature = (
            wallet.sign(
                transaction.signing_payload(),
                password,
            )
        )

        return transaction


def validate_transaction(
    transaction: Transaction,
):

    # -----------------------------------------------------
    # Basic validation
    # -----------------------------------------------------

    if not transaction.transaction_id:
        return False, "Missing transaction ID."

    if not transaction.sender:
        return False, "Missing sender."

    if not transaction.receiver:
        return False, "Missing receiver."

    if transaction.sender == transaction.receiver:
        return False, "Sender and receiver cannot be identical."

    # -----------------------------------------------------
    # Amount validation
    # -----------------------------------------------------

    try:

        amount = Decimal(
            transaction.amount
        )

    except InvalidOperation:

        return False, "Invalid amount."

    if amount <= 0:

        return False, "Amount must be positive."

    if amount.as_tuple().exponent < -2:

        return False, (
            "PYC supports a maximum of 2 decimal places."
        )

    # -----------------------------------------------------
    # Address verification
    # -----------------------------------------------------

    try:

        public_key = b64_decode(
            transaction.public_key
        )

        expected_address = (
            public_key_to_address(
                public_key
            )
        )

        if expected_address != transaction.sender:

            return False, (
                "Sender address does not match public key."
            )

    except Exception:

        return False, "Invalid public key."

    # -----------------------------------------------------
    # Digital signature
    # -----------------------------------------------------

    try:

        signature = b64_decode(
            transaction.signature
        )

    except Exception:

        return False, "Invalid signature encoding."

    valid_signature = verify_signature(
        public_key,
        signature,
        transaction.signing_payload(),
    )

    if not valid_signature:

        return False, (
            "Digital signature verification failed."
        )

    return True, "Transaction verified successfully."