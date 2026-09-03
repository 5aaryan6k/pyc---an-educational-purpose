import getpass
import time
import uuid
from decimal import Decimal, InvalidOperation

from config import (
    DATABASE_FILE,
    INITIAL_BALANCE,
    COIN_NAME,
)

from core.blockchain import Blockchain
from core.crypto import (
    hash_password,
    verify_password,
)

from core.transaction import (
    Transaction,
    validate_transaction,
)

from core.wallet import Wallet

from database.database import Database

from invoice.invoice import (
    generate_invoice,
)


class PYCApplication:

    def __init__(self):

        self.database = Database(
            DATABASE_FILE
        )

        self.blockchain = (
            Blockchain()
        )

        stored_blocks = (
            self.database.load_blocks()
        )

        if stored_blocks:

            self.blockchain.chain = (
                stored_blocks
            )

        self.current_user = None

        self.login_password = None

    # =====================================================
    # Persistence
    # =====================================================

    def save_blockchain(self):

        for block in (
            self.blockchain.chain
        ):

            self.database.save_block(
                block
            )

    # =====================================================
    # Registration
    # =====================================================

    def register(self):

        print()
        print("=" * 60)
        print("CREATE PYC ACCOUNT")
        print("=" * 60)

        username = (
            input("Username: ")
            .strip()
            .lower()
        )

        if len(username) < 3:

            print(
                "Username must contain at least 3 characters."
            )

            return

        if self.database.user_exists(
            username
        ):

            print(
                "Username already exists."
            )

            return

        password = getpass.getpass(
            "Password: "
        )

        confirm = getpass.getpass(
            "Confirm password: "
        )

        if password != confirm:

            print(
                "Passwords do not match."
            )

            return

        if len(password) < 8:

            print(
                "Password must contain at least 8 characters."
            )

            return

        # -------------------------------------------------
        # Generate wallet
        # -------------------------------------------------

        wallet = Wallet.create(
            password
        )

        password_salt, password_hash = (
            hash_password(password)
        )

        # -------------------------------------------------
        # Store account
        # -------------------------------------------------

        self.database.create_user(
            username,
            password_salt,
            password_hash,
            wallet,
        )

        # -------------------------------------------------
        # Educational faucet
        # -------------------------------------------------

        self.blockchain.create_initial_balance(
            wallet.address
        )

        self.save_blockchain()

        print()
        print("Account successfully created.")
        print()
        print("Username:")
        print(username)

        print()
        print("Wallet address:")
        print(wallet.address)

        print()
        print("Initial PYC balance:")
        print(
            f"{INITIAL_BALANCE} {COIN_NAME}"
        )

        print()
        print(
            "IMPORTANT: Keep your password safe."
        )

    # =====================================================
    # Login
    # =====================================================

    def login(self):

        print()
        print("=" * 60)
        print("PYC LOGIN")
        print("=" * 60)

        username = (
            input("Username: ")
            .strip()
            .lower()
        )

        user = self.database.get_user(
            username
        )

        if not user:

            print(
                "Invalid username or password."
            )

            return False

        password = getpass.getpass(
            "Password: "
        )

        if not verify_password(
            password,
            user["password_salt"],
            user["password_hash"],
        ):

            print(
                "Invalid username or password."
            )

            return False

        self.current_user = user

        # Keep password in memory only
        # for signing during this session.
        self.login_password = password

        print()
        print(
            f"Welcome, {username}!"
        )

        return True

    # =====================================================
    # Logout
    # =====================================================

    def logout(self):

        self.current_user = None
        self.login_password = None

        print(
            "Logged out successfully."
        )

    # =====================================================
    # Wallet
    # =====================================================

    def wallet(self):

        address = (
            self.current_user["address"]
        )

        balance = (
            self.blockchain.get_balance(
                address
            )
        )

        print()
        print("=" * 60)
        print("MY WALLET")
        print("=" * 60)

        print(
            "Username:",
            self.current_user["username"],
        )

        print(
            "Address:",
            address,
        )

        print(
            "Balance:",
            f"{balance:.2f} PYC",
        )

    # =====================================================
    # Receive
    # =====================================================

    def receive(self):

        print()
        print("=" * 60)
        print("RECEIVE PYC")
        print("=" * 60)

        print()
        print(
            "Give this address to the sender:"
        )

        print()

        print(
            self.current_user["address"]
        )

        print()

        print(
            "Anyone sending PYC to this address"
            " will be credited after the transaction"
            " is verified and mined."
        )

    # =====================================================
    # Verify wallet
    # =====================================================

    def verify_wallet(self):

        print()
        print("=" * 60)
        print("VERIFY WALLET")
        print("=" * 60)

        address = (
            input("PYC address: ")
            .strip()
        )

        user = (
            self.database.get_user_by_address(
                address
            )
        )

        if not user:

            print()
            print(
                "No local account found for this address."
            )

            return

        balance = (
            self.blockchain.get_balance(
                address
            )
        )

        print()
        print("✓ Wallet exists")
        print(
            "Username:",
            user["username"],
        )

        print(
            "Address:",
            address,
        )

        print(
            "Balance:",
            f"{balance:.2f} PYC",
        )

    # =====================================================
    # Send PYC
    # =====================================================

    def send_pyc(self):

        print()
        print("=" * 60)
        print("SEND PYC")
        print("=" * 60)

        sender = (
            self.current_user["address"]
        )

        receiver = (
            input(
                "Receiver wallet address: "
            )
            .strip()
        )

        # -------------------------------------------------
        # Verify receiver
        # -------------------------------------------------

        receiver_user = (
            self.database.get_user_by_address(
                receiver
            )
        )

        if not receiver_user:

            print()
            print(
                "Receiver wallet was not found."
            )

            print(
                "Use 'Verify Wallet' first."
            )

            return

        if receiver == sender:

            print(
                "You cannot send PYC to yourself."
            )

            return

        # -------------------------------------------------
        # Amount
        # -------------------------------------------------

        amount_text = input(
            "Amount PYC: "
        ).strip()

        try:

            amount = Decimal(
                amount_text
            ).quantize(
                Decimal("0.01")
            )

        except InvalidOperation:

            print(
                "Invalid amount."
            )

            return

        if amount <= 0:

            print(
                "Amount must be greater than 0."
            )

            return

        # -------------------------------------------------
        # Balance
        # -------------------------------------------------

        balance = (
            self.blockchain.get_balance(
                sender
            )
        )

        print()
        print(
            f"Available balance: "
            f"{balance:.2f} PYC"
        )

        if amount > balance:

            print()
            print(
                "✗ Transaction rejected."
            )

            print(
                "Reason: insufficient balance."
            )

            return

        # -------------------------------------------------
        # Optional invoice
        # -------------------------------------------------

        invoice_id = input(
            "Invoice ID (optional): "
        ).strip()

        if not invoice_id:

            invoice_id = None

        else:

            invoice = (
                self.database.get_invoice(
                    invoice_id
                )
            )

            if not invoice:

                print(
                    "Invoice does not exist."
                )

                return

            if invoice["status"] == "PAID":

                print(
                    "Invoice has already been paid."
                )

                return

            if Decimal(
                invoice["amount"]
            ) != amount:

                print(
                    "Amount does not match invoice."
                )

                return

        # -------------------------------------------------
        # Load wallet
        # -------------------------------------------------

        wallet = Wallet(
            address=self.current_user[
                "address"
            ],

            public_key=self.current_user[
                "public_key"
            ],

            encrypted_private_key=(
                self.current_user[
                    "encrypted_private_key"
                ]
            ),

            encryption_salt=(
                self.current_user[
                    "encryption_salt"
                ]
            ),
        )

        # -------------------------------------------------
        # Create signed transaction
        # -------------------------------------------------

        transaction = Transaction.create(
            sender=sender,
            receiver=receiver,
            amount=amount,
            wallet=wallet,
            password=self.login_password,
            invoice_id=invoice_id,
        )

        print()
        print(
            "Verifying transaction..."
        )

        valid, message = (
            validate_transaction(
                transaction
            )
        )

        if not valid:

            print(
                "✗ Verification failed:"
            )

            print(message)

            return

        print(
            "✓ Digital signature verified."
        )

        # -------------------------------------------------
        # Mine
        # -------------------------------------------------

        print()
        print(
            "Mining transaction..."
        )

        try:

            block = (
                self.blockchain.add_transaction(
                    transaction
                )
            )

        except ValueError as error:

            print()
            print(
                "✗ Transaction rejected:"
            )

            print(error)

            return

        self.save_blockchain()

        # -------------------------------------------------
        # Invoice payment
        # -------------------------------------------------

        if invoice_id:

            self.database.mark_invoice_paid(
                invoice_id,
                transaction.transaction_id,
            )

        # -------------------------------------------------
        # Success
        # -------------------------------------------------

        print()
        print("=" * 60)
        print("✓ PAYMENT SUCCESSFUL")
        print("=" * 60)

        print(
            "Transaction ID:",
            transaction.transaction_id,
        )

        print(
            "From:",
            transaction.sender,
        )

        print(
            "To:",
            transaction.receiver,
        )

        print(
            "Amount:",
            f"{transaction.amount} PYC",
        )

        print(
            "Block:",
            block.index,
        )

        print(
            "Block hash:",
            block.hash,
        )

        print(
            "New balance:",
            f"{self.blockchain.get_balance(sender):.2f} PYC",
        )

    # =====================================================
    # Create invoice
    # =====================================================

    def create_invoice(self):

        print()
        print("=" * 60)
        print("CREATE INVOICE")
        print("=" * 60)

        receiver = (
            input(
                "Customer wallet address: "
            )
            .strip()
        )

        receiver_user = (
            self.database.get_user_by_address(
                receiver
            )
        )

        if not receiver_user:

            print(
                "Customer wallet not found."
            )

            return

        amount_text = input(
            "Amount PYC: "
        ).strip()

        try:

            amount = Decimal(
                amount_text
            ).quantize(
                Decimal("0.01")
            )

        except InvalidOperation:

            print(
                "Invalid amount."
            )

            return

        if amount <= 0:

            print(
                "Amount must be greater than zero."
            )

            return

        description = input(
            "Description: "
        ).strip()

        invoice_id = (
            "INV-"
            + time.strftime("%Y%m%d")
            + "-"
            + uuid.uuid4().hex[:8].upper()
        )

        created_at = time.time()

        self.database.create_invoice(
            invoice_id,
            self.current_user["address"],
            receiver,
            f"{amount:.2f}",
            description,
            created_at,
        )

        filename = generate_invoice(
            invoice_id,
            self.current_user["address"],
            receiver,
            f"{amount:.2f}",
            description,
            "PENDING",
            time.ctime(created_at),
        )

        print()
        print(
            "✓ Invoice created."
        )

        print(
            "Invoice ID:",
            invoice_id,
        )

        print(
            "Invoice file:",
            filename,
        )

    # =====================================================
    # View invoice
    # =====================================================

    def view_invoice(self):

        print()
        print("=" * 60)
        print("VIEW INVOICE")
        print("=" * 60)

        invoice_id = input(
            "Invoice ID: "
        ).strip()

        invoice = (
            self.database.get_invoice(
                invoice_id
            )
        )

        if not invoice:

            print(
                "Invoice not found."
            )

            return

        print()
        print(
            "Invoice ID:",
            invoice["invoice_id"],
        )

        print(
            "From:",
            invoice["sender"],
        )

        print(
            "To:",
            invoice["receiver"],
        )

        print(
            "Amount:",
            invoice["amount"],
            "PYC",
        )

        print(
            "Description:",
            invoice["description"],
        )

        print(
            "Status:",
            invoice["status"],
        )

        print(
            "Transaction:",
            invoice["paid_transaction_id"]
            or "Not paid",
        )

    # =====================================================
    # History
    # =====================================================

    def history(self):

        print()
        print("=" * 60)
        print("TRANSACTION HISTORY")
        print("=" * 60)

        address = (
            self.current_user["address"]
        )

        transactions = (
            self.blockchain.get_history(
                address
            )
        )

        if not transactions:

            print(
                "No transactions found."
            )

            return

        for transaction in reversed(
            transactions
        ):

            if (
                transaction.sender
                == address
            ):

                direction = "SENT"

                counterparty = (
                    transaction.receiver
                )

            else:

                direction = "RECEIVED"

                counterparty = (
                    transaction.sender
                )

            valid, _ = (
                validate_transaction(
                    transaction
                )
            )

            print()
            print("-" * 60)

            print(
                "Type:",
                direction,
            )

            print(
                "Transaction:",
                transaction.transaction_id,
            )

            print(
                "Counterparty:",
                counterparty,
            )

            print(
                "Amount:",
                transaction.amount,
                "PYC",
            )

            print(
                "Invoice:",
                transaction.invoice_id
                or "None",
            )

            print(
                "Verified:",
                "YES" if valid else "NO",
            )

            print(
                "Time:",
                time.ctime(
                    transaction.timestamp
                ),
            )

    # =====================================================
    # Blockchain verification
    # =====================================================

    def verify_blockchain(self):

        print()
        print("=" * 60)
        print("BLOCKCHAIN VERIFICATION")
        print("=" * 60)

        valid, message = (
            self.blockchain.verify_chain()
        )

        print()

        if valid:

            print(
                "✓",
                message,
            )

            print(
                "Total blocks:",
                len(
                    self.blockchain.chain
                ),
            )

        else:

            print(
                "✗",
                message,
            )

    # =====================================================
    # Blockchain explorer
    # =====================================================

    def explorer(self):

        print()
        print("=" * 60)
        print("PYC BLOCKCHAIN EXPLORER")
        print("=" * 60)

        for block in (
            self.blockchain.chain
        ):

            print()
            print("-" * 60)

            print(
                "Block:",
                block.index,
            )

            print(
                "Hash:",
                block.hash,
            )

            print(
                "Previous:",
                block.previous_hash,
            )

            print(
                "Nonce:",
                block.nonce,
            )

            print(
                "Transactions:",
                len(
                    block.transactions
                ),
            )

    # =====================================================
    # User menu
    # =====================================================

    def user_menu(self):

        while self.current_user:

            print()
            print("=" * 60)
            print("PYC WALLET")
            print("=" * 60)

            print("""
1. My Wallet / Balance
2. Send PYC
3. Receive PYC
4. Verify Wallet
5. Create Invoice
6. View Invoice
7. Transaction History
8. Verify Blockchain
9. Blockchain Explorer
0. Logout
""")

            choice = input(
                "Choose: "
            ).strip()

            if choice == "1":

                self.wallet()

            elif choice == "2":

                self.send_pyc()

            elif choice == "3":

                self.receive()

            elif choice == "4":

                self.verify_wallet()

            elif choice == "5":

                self.create_invoice()

            elif choice == "6":

                self.view_invoice()

            elif choice == "7":

                self.history()

            elif choice == "8":

                self.verify_blockchain()

            elif choice == "9":

                self.explorer()

            elif choice == "0":

                self.logout()

            else:

                print(
                    "Invalid option."
                )

    # =====================================================
    # Main menu
    # =====================================================

    def run(self):

        print()
        print("=" * 60)
        print("              PYC BLOCKCHAIN")
        print("=" * 60)
        print("        Educational Cryptocurrency")
        print("=" * 60)

        while True:

            print("""
1. Register
2. Login
3. Verify Blockchain
0. Exit
""")

            choice = input(
                "Choose: "
            ).strip()

            if choice == "1":

                self.register()

            elif choice == "2":

                if self.login():

                    self.user_menu()

            elif choice == "3":

                self.verify_blockchain()

            elif choice == "0":

                print(
                    "Goodbye."
                )

                break

            else:

                print(
                    "Invalid option."
                )


if __name__ == "__main__":

    application = (
        PYCApplication()
    )

    application.run()