import json
import sqlite3

from core.block import Block


class Database:

    def __init__(
        self,
        filename,
    ):

        self.connection = (
            sqlite3.connect(filename)
        )

        self.connection.row_factory = (
            sqlite3.Row
        )

        self.create_tables()

    # =====================================================
    # Tables
    # =====================================================

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                address TEXT UNIQUE NOT NULL,
                public_key TEXT NOT NULL,
                encrypted_private_key TEXT NOT NULL,
                encryption_salt TEXT NOT NULL,
                created_at REAL NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                invoice_id TEXT PRIMARY KEY,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                amount TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                created_at REAL NOT NULL,
                paid_transaction_id TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blocks (
                block_index INTEGER PRIMARY KEY,
                block_json TEXT NOT NULL
            )
        """)

        self.connection.commit()

    # =====================================================
    # Users
    # =====================================================

    def user_exists(
        self,
        username,
    ):

        cursor = self.connection.cursor()

        result = cursor.execute(
            """
            SELECT username
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

        return result is not None

    def create_user(
        self,
        username,
        password_salt,
        password_hash,
        wallet,
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password_salt,
                password_hash,
                address,
                public_key,
                encrypted_private_key,
                encryption_salt,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                password_salt,
                password_hash,
                wallet.address,
                wallet.public_key,
                wallet.encrypted_private_key,
                wallet.encryption_salt,
                __import__("time").time(),
            ),
        )

        self.connection.commit()

    def get_user(
        self,
        username,
    ):

        cursor = self.connection.cursor()

        return cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

    def get_user_by_address(
        self,
        address,
    ):

        cursor = self.connection.cursor()

        return cursor.execute(
            """
            SELECT *
            FROM users
            WHERE address = ?
            """,
            (address,),
        ).fetchone()

    # =====================================================
    # Invoice
    # =====================================================

    def create_invoice(
        self,
        invoice_id,
        sender,
        receiver,
        amount,
        description,
        created_at,
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO invoices
            (
                invoice_id,
                sender,
                receiver,
                amount,
                description,
                status,
                created_at,
                paid_transaction_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                invoice_id,
                sender,
                receiver,
                amount,
                description,
                "PENDING",
                created_at,
                None,
            ),
        )

        self.connection.commit()

    def get_invoice(
        self,
        invoice_id,
    ):

        cursor = self.connection.cursor()

        return cursor.execute(
            """
            SELECT *
            FROM invoices
            WHERE invoice_id = ?
            """,
            (invoice_id,),
        ).fetchone()

    def mark_invoice_paid(
        self,
        invoice_id,
        transaction_id,
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE invoices
            SET status = 'PAID',
                paid_transaction_id = ?
            WHERE invoice_id = ?
            """,
            (
                transaction_id,
                invoice_id,
            ),
        )

        self.connection.commit()

    # =====================================================
    # Blockchain persistence
    # =====================================================

    def save_block(
        self,
        block: Block,
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO blocks
            (
                block_index,
                block_json
            )
            VALUES (?, ?)
            """,
            (
                block.index,
                json.dumps(
                    {
                        "index": block.index,
                        "timestamp": block.timestamp,
                        "transactions": block.transactions,
                        "previous_hash": block.previous_hash,
                        "nonce": block.nonce,
                        "hash": block.hash,
                    }
                ),
            ),
        )

        self.connection.commit()

    def load_blocks(self):

        cursor = self.connection.cursor()

        rows = cursor.execute(
            """
            SELECT block_json
            FROM blocks
            ORDER BY block_index ASC
            """
        ).fetchall()

        blocks = []

        for row in rows:

            data = json.loads(
                row["block_json"]
            )

            blocks.append(
                Block(**data)
            )

        return blocks