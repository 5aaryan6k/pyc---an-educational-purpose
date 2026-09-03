from decimal import Decimal

from config import (
    DIFFICULTY,
    INITIAL_BALANCE,
)

from core.block import Block
from core.transaction import (
    Transaction,
    validate_transaction,
)


class Blockchain:

    def __init__(self):

        self.chain = []

        self.create_genesis_block()

    # =====================================================
    # Genesis
    # =====================================================

    def create_genesis_block(self):

        genesis_transactions = [
            {
                "type": "GENESIS",
                "message": "PYC Genesis Block",
            }
        ]

        genesis = Block.mine(
            index=0,
            transactions=genesis_transactions,
            previous_hash="0",
            difficulty=DIFFICULTY,
        )

        self.chain.append(
            genesis
        )

    # =====================================================
    # Latest block
    # =====================================================

    @property
    def latest_block(self):

        return self.chain[-1]

    # =====================================================
    # Faucet
    # =====================================================

    def create_initial_balance(
        self,
        address,
    ):

        transaction = {
            "type": "FAUCET",
            "address": address,
            "amount": str(
                INITIAL_BALANCE
            ),
        }

        block = Block.mine(
            index=len(self.chain),
            transactions=[transaction],
            previous_hash=self.latest_block.hash,
            difficulty=DIFFICULTY,
        )

        self.chain.append(
            block
        )

        return block

    # =====================================================
    # Calculate balance
    # =====================================================

    def get_balance(
        self,
        address,
    ):

        balance = Decimal("0.00")

        for block in self.chain:

            for raw in block.transactions:

                transaction_type = (
                    raw.get("type")
                )

                # -----------------------------------------
                # Faucet
                # -----------------------------------------

                if transaction_type == "FAUCET":

                    if raw["address"] == address:

                        balance += Decimal(
                            raw["amount"]
                        )

                    continue

                # -----------------------------------------
                # Genesis
                # -----------------------------------------

                if transaction_type == "GENESIS":

                    continue

                # -----------------------------------------
                # Normal transaction
                # -----------------------------------------

                transaction = (
                    Transaction(**raw)
                )

                amount = Decimal(
                    transaction.amount
                )

                if transaction.sender == address:

                    balance -= amount

                if transaction.receiver == address:

                    balance += amount

        return balance.quantize(
            Decimal("0.01")
        )

    # =====================================================
    # Verify sender balance
    # =====================================================

    def has_sufficient_balance(
        self,
        address,
        amount,
    ):

        amount = Decimal(
            str(amount)
        )

        return (
            self.get_balance(address)
            >= amount
        )

    # =====================================================
    # Add transaction
    # =====================================================

    def add_transaction(
        self,
        transaction: Transaction,
    ):

        # -------------------------------------------------
        # Verify transaction signature
        # -------------------------------------------------

        valid, message = (
            validate_transaction(
                transaction
            )
        )

        if not valid:

            raise ValueError(
                message
            )

        # -------------------------------------------------
        # Verify sender balance
        # -------------------------------------------------

        amount = Decimal(
            transaction.amount
        )

        if not self.has_sufficient_balance(
            transaction.sender,
            amount,
        ):

            raise ValueError(
                "Insufficient PYC balance."
            )

        # -------------------------------------------------
        # Prevent duplicate transaction
        # -------------------------------------------------

        if self.transaction_exists(
            transaction.transaction_id
        ):

            raise ValueError(
                "Transaction already exists."
            )

        # -------------------------------------------------
        # Mine transaction
        # -------------------------------------------------

        block = Block.mine(
            index=len(self.chain),
            transactions=[
                transaction.to_dict()
            ],
            previous_hash=self.latest_block.hash,
            difficulty=DIFFICULTY,
        )

        self.chain.append(
            block
        )

        return block

    # =====================================================
    # Transaction lookup
    # =====================================================

    def transaction_exists(
        self,
        transaction_id,
    ):

        for block in self.chain:

            for raw in block.transactions:

                if (
                    raw.get("transaction_id")
                    == transaction_id
                ):

                    return True

        return False

    # =====================================================
    # Find transaction
    # =====================================================

    def find_transaction(
        self,
        transaction_id,
    ):

        for block in self.chain:

            for raw in block.transactions:

                if (
                    raw.get("transaction_id")
                    == transaction_id
                ):

                    return (
                        raw,
                        block,
                    )

        return None, None

    # =====================================================
    # History
    # =====================================================

    def get_history(
        self,
        address,
    ):

        history = []

        for block in self.chain:

            for raw in block.transactions:

                if raw.get("type") in (
                    "GENESIS",
                    "FAUCET",
                ):

                    continue

                transaction = (
                    Transaction(**raw)
                )

                if (
                    transaction.sender
                    == address
                    or
                    transaction.receiver
                    == address
                ):

                    history.append(
                        transaction
                    )

        return history

    # =====================================================
    # Full blockchain verification
    # =====================================================

    def verify_chain(self):

        if not self.chain:

            return False, (
                "Blockchain is empty."
            )

        calculated_balances = {}

        for index, block in enumerate(
            self.chain
        ):

            # ---------------------------------------------
            # Verify block hash
            # ---------------------------------------------

            if (
                block.hash
                != block.calculate_hash()
            ):

                return False, (
                    f"Block {index} hash is invalid."
                )

            # ---------------------------------------------
            # Verify PoW
            # ---------------------------------------------

            if not block.hash.startswith(
                "0" * DIFFICULTY
            ):

                return False, (
                    f"Block {index} fails Proof of Work."
                )

            # ---------------------------------------------
            # Previous hash
            # ---------------------------------------------

            if index == 0:

                if block.previous_hash != "0":

                    return False, (
                        "Invalid genesis block."
                    )

            else:

                previous_block = (
                    self.chain[index - 1]
                )

                if (
                    block.previous_hash
                    != previous_block.hash
                ):

                    return False, (
                        f"Block {index} previous hash is invalid."
                    )

            # ---------------------------------------------
            # Transactions
            # ---------------------------------------------

            for raw in block.transactions:

                transaction_type = (
                    raw.get("type")
                )

                if transaction_type == "GENESIS":

                    continue

                if transaction_type == "FAUCET":

                    address = raw["address"]

                    amount = Decimal(
                        raw["amount"]
                    )

                    calculated_balances[
                        address
                    ] = calculated_balances.get(
                        address,
                        Decimal("0.00"),
                    ) + amount

                    continue

                transaction = (
                    Transaction(**raw)
                )

                valid, message = (
                    validate_transaction(
                        transaction
                    )
                )

                if not valid:

                    return False, (
                        f"Invalid transaction "
                        f"{transaction.transaction_id}: "
                        f"{message}"
                    )

                amount = Decimal(
                    transaction.amount
                )

                sender_balance = (
                    calculated_balances.get(
                        transaction.sender,
                        Decimal("0.00"),
                    )
                )

                if sender_balance < amount:

                    return False, (
                        "Blockchain contains an "
                        "overspending transaction."
                    )

                calculated_balances[
                    transaction.sender
                ] = (
                    sender_balance
                    - amount
                )

                calculated_balances[
                    transaction.receiver
                ] = (
                    calculated_balances.get(
                        transaction.receiver,
                        Decimal("0.00"),
                    )
                    + amount
                )

        return True, (
            "Blockchain verified successfully."
        )