from decimal import Decimal

COIN_NAME = "PYC"

DATABASE_FILE = "pyc.db"
BLOCKCHAIN_FILE = "blockchain.json"

# Number of leading zeroes required by Proof of Work.
DIFFICULTY = 4

# Educational faucet amount for newly registered wallets.
INITIAL_BALANCE = Decimal("100.00")

# Minimum transaction amount.
MIN_TRANSACTION = Decimal("0.01")