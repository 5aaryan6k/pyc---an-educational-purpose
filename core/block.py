import hashlib
import json
import time

from dataclasses import dataclass


@dataclass
class Block:

    index: int

    timestamp: float

    transactions: list

    previous_hash: str

    nonce: int

    hash: str

    def calculate_hash(self):

        data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }

        serialized = json.dumps(
            data,
            sort_keys=True,
            separators=(",", ":"),
        )

        return hashlib.sha256(
            serialized.encode()
        ).hexdigest()

    @classmethod
    def mine(
        cls,
        index,
        transactions,
        previous_hash,
        difficulty,
    ):

        timestamp = time.time()

        nonce = 0

        prefix = "0" * difficulty

        while True:

            block = cls(
                index=index,
                timestamp=timestamp,
                transactions=transactions,
                previous_hash=previous_hash,
                nonce=nonce,
                hash="",
            )

            block.hash = (
                block.calculate_hash()
            )

            if block.hash.startswith(prefix):

                return block

            nonce += 1