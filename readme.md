# 🪙 PYC Blockchain - Educational Cryptocurrency System

> ⚠️ **EDUCATIONAL USE ONLY**
>
> **PYC Blockchain is an educational and research project created to demonstrate blockchain, cryptocurrency, cryptography, digital signatures, wallets, transactions, and Proof-of-Work concepts.**
>
> PYC is **not a real cryptocurrency and has no monetary value**. This software is not intended for real financial transactions, production cryptocurrency systems, or the storage of real funds or sensitive financial information.
>
> **Use this project only for educational, development, testing, and demonstration purposes.**


A complete **Python-based educational cryptocurrency and blockchain system** with wallets, digital signatures, transactions, Proof-of-Work mining, balance verification, invoices, SQLite persistence, and a command-line interface.

> **PYC** is an educational cryptocurrency created to demonstrate how blockchain-based digital currency systems work using Python.

---

## Table of Contents

* [About the Project](#-about-the-project)
* [Project Objectives](#-project-objectives)
* [Features](#-features)
* [Technology Stack](#-technology-stack)
* [Project Architecture](#-project-architecture)
* [Requirements](#-requirements)
* [Installation](#-installation)
* [Running the Application](#-running-the-application)
* [First-Time Setup](#-first-time-setup)
* [CLI Menu](#-cli-menu)
* [Wallet System](#-wallet-system)
* [Sending PYC](#-sending-pyc)
* [Receiving PYC](#-receiving-pyc)
* [Transaction Verification](#-transaction-verification)
* [Mining](#-mining)
* [Proof of Work](#-proof-of-work)
* [Invoices](#-invoices)
* [Blockchain Verification](#-blockchain-verification)
* [Blockchain Explorer](#-blockchain-explorer)
* [Database](#-database)
* [Security](#-security)
* [Project Structure](#-project-structure)
* [Configuration](#-configuration)
* [Useful Commands](#-useful-commands)
* [Troubleshooting](#-troubleshooting)
* [Limitations](#-limitations)
* [Future Improvements](#-future-improvements)
* [Educational Purpose](#-educational-purpose)
* [License](#-license)

---

# About the Project

PYC Blockchain is a **local, single-node blockchain cryptocurrency prototype** developed in Python.

The system demonstrates the fundamental components required for a cryptocurrency:

* Blockchain
* Blocks
* Transactions
* Wallets
* Public/private key cryptography
* Digital signatures
* Proof-of-Work
* Mining
* Balance calculation
* Transaction verification
* Invoice generation
* Persistent storage
* Command-line interaction

The project is designed primarily for **learning, experimentation, coursework, demonstrations, and understanding blockchain architecture**.

---

# Project Objectives

The main objectives of PYC Blockchain are to demonstrate:

1. How blockchain blocks are created.
2. How transactions are represented.
3. How wallets are generated.
4. How public/private key cryptography works.
5. How transactions can be digitally signed.
6. How transaction authenticity can be verified.
7. How Proof-of-Work mining operates.
8. How wallet balances can be calculated.
9. How double spending can be detected.
10. How invoices can be generated and associated with transactions.
11. How blockchain integrity can be verified.
12. How blockchain data can be stored persistently.

---

# Features

## User Authentication

* User registration
* Login
* Logout
* Password hashing
* Password-based private-key encryption

## Wallet

Each registered user receives a PYC wallet containing:

* Wallet address
* Public key
* Encrypted private key
* Wallet balance

Wallet addresses are derived from the wallet's public key.

## Transactions

Users can:

* Send PYC
* Specify recipient wallet
* Specify transaction amount
* Digitally sign transactions
* Verify transactions
* View transaction history

## Transaction Security

Transactions use:

* Ed25519 digital signatures
* SHA-256 hashing
* Public/private key cryptography
* Sender address verification
* Balance verification

## Mining

Transactions are grouped into blocks.

Blocks are mined using Proof-of-Work.

The default mining difficulty requires the block hash to begin with:

```text
0000
```

## Invoices

Users can create invoices containing:

* Invoice ID
* Seller wallet
* Customer wallet
* Amount
* Description
* Creation date
* Payment status

Invoices can be associated with blockchain transactions.

## Blockchain Verification

The system can verify:

* Block hashes
* Previous block hashes
* Proof-of-Work
* Transaction signatures
* Transaction integrity
* Wallet balances
* Overspending
* Duplicate transactions

## Persistent Storage

SQLite is used to store application data locally.

The system can persist:

* Users
* Wallet information
* Invoices
* Blockchain blocks

---

# Technology Stack

| Technology         | Purpose                       |
| ------------------ | ----------------------------- |
| Python 3           | Core programming language     |
| SQLite             | Local database                |
| SHA-256            | Hashing                       |
| Ed25519            | Digital signatures            |
| AES-GCM            | Private-key encryption        |
| PBKDF2-HMAC-SHA256 | Password-based key derivation |
| Proof-of-Work      | Block mining                  |
| Cryptography       | Cryptographic operations      |
| CLI                | User interface                |

---

# Project Architecture

The project is divided into several modules.

```text
User
 │
 ▼
CLI (main.py)
 │
 ├── Authentication
 │
 ├── Wallet
 │
 ├── Transactions
 │
 ├── Invoices
 │
 └── Blockchain
        │
        ├── Block
        ├── Proof-of-Work
        ├── Transaction Verification
        └── Chain Verification
                 │
                 ▼
              SQLite
```

---

# Project Structure

```text
pycproject/
│
├── main.py
├── config.py
├── requirements.txt
├── README.md
│
├── core/
│   ├── __init__.py
│   ├── crypto.py
│   ├── wallet.py
│   ├── transaction.py
│   ├── block.py
│   └── blockchain.py
│
├── database/
│   ├── __init__.py
│   └── database.py
│
├── invoice/
│   ├── __init__.py
│   └── invoice.py
│
├── invoices/
│
└── data/
```

### Core modules

#### `core/crypto.py`

Handles cryptographic functionality:

* Key generation
* Digital signatures
* Signature verification
* Password hashing
* Private-key encryption/decryption

#### `core/wallet.py`

Handles:

* Wallet creation
* Wallet addresses
* Public/private keys
* Private-key protection

#### `core/transaction.py`

Handles:

* Transaction creation
* Transaction signing
* Transaction validation
* Transaction IDs

#### `core/block.py`

Handles:

* Block creation
* Block hashing
* Nonce
* Timestamp
* Proof-of-Work

#### `core/blockchain.py`

Handles:

* Blockchain creation
* Genesis block
* Transaction processing
* Mining
* Balance calculation
* Chain verification

#### `database/database.py`

Handles SQLite persistence.

#### `invoice/invoice.py`

Handles invoice generation and invoice files.

#### `main.py`

Provides the interactive command-line interface.

---

# Requirements

Before installing PYC Blockchain, make sure you have:

* Python 3.10 or newer
* pip
* PowerShell / Command Prompt / Terminal
* Git (optional)

Check Python:

```powershell
python --version
```

Example:

```text
Python 3.12.4
```

Check pip:

```powershell
python -m pip --version
```

---

# Installation

## Step 1 — Clone or download the project

If using Git:

```powershell
git clone <YOUR-REPOSITORY-URL>
```

Then:

```powershell
cd pycproject
```

Or simply open the project folder in VS Code.

---

# Step 2 — Create a Virtual Environment

Creating a virtual environment keeps project dependencies isolated.

Run:

```powershell
python -m venv venv
```

---

# ▶Step 3 — Activate the Virtual Environment

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

After activation, you should see:

```text
(venv) PS A:\projects\FYP IDEAS\PyC\pycproject>
```

### Windows CMD

```cmd
venv\Scripts\activate
```

---

# Step 4 — Install Dependencies

Install all required packages:

```powershell
python -m pip install -r requirements.txt
```

If `requirements.txt` does not exist or you only need the cryptography package:

```powershell
python -m pip install cryptography
```

Verify installation:

```powershell
python -c "import cryptography; print(cryptography.__version__)"
```

You should receive a version number.

---

# Running the Application

Once the virtual environment is activated:

```powershell
python main.py
```

You should see the PYC Blockchain CLI.

Example:

```text
========================================
        PYC BLOCKCHAIN
========================================

1. Register
2. Login
3. Exit

Select an option:
```

---

# First-Time Setup

## 1. Register

Choose:

```text
1
```

Enter your:

```text
Username
Password
```

The system creates a wallet for the new user.

---

## 2. Login

Choose:

```text
2
```

Enter the credentials created during registration.

After successful authentication, the main wallet menu becomes available.

---

# CLI Menu

After logging in, the application provides options similar to:

```text
========================================
              PYC WALLET
========================================

1. Wallet / Balance
2. Send PYC
3. Receive PYC
4. Verify Wallet
5. Create Invoice
6. View Invoice
7. Transaction History
8. Verify Blockchain
9. Blockchain Explorer
10. Logout

Select an option:
```

Enter the corresponding number and press:

```text
Enter
```

---

# Wallet System

Each user receives a unique wallet.

A wallet contains:

```text
Wallet Address
Public Key
Encrypted Private Key
```

Example wallet address:

```text
PYC7a9f4b8e21c...
```

The wallet address is derived from the public key.

The private key is **not stored as plain text**.

It is encrypted using a password-derived encryption key.

---

# Checking Your Balance

Select:

```text
1. Wallet / Balance
```

The system calculates your current PYC balance from blockchain transactions.

Example:

```text
Wallet:
PYC7a9f4b8e21c...

Balance:
100.00 PYC
```

---

# Sending PYC

To send PYC:

```text
2. Send PYC
```

The system asks for:

```text
Recipient wallet address
Amount
```

Example:

```text
Recipient: PYCabc123...
Amount: 10
```

The system then:

1. Checks the recipient address.
2. Checks your wallet balance.
3. Creates a transaction.
4. Signs the transaction using your private key.
5. Verifies the signature.
6. Adds the transaction to the blockchain.
7. Mines a block.
8. Updates the blockchain state.

---

# Receiving PYC

To receive PYC:

```text
3. Receive PYC
```

The system displays your wallet address.

Example:

```text
Your PYC wallet address:

PYC7a9f4b8e21c...

Give this address to the sender.
```

The receiver does **not** manually create a receiving transaction.

The sender creates the transaction using the receiver's wallet address.

---

# Transaction Verification

Every transaction contains information such as:

```text
Transaction ID
Sender
Receiver
Amount
Timestamp
Public Key
Signature
```

Before a transaction is accepted, the system verifies:

### 1. Sender identity

The public key must correspond to the sender wallet.

### 2. Digital signature

The signature must be valid.

### 3. Transaction amount

The amount must be positive.

### 4. Balance

The sender must have sufficient PYC.

### 5. Duplicate transaction

The transaction must not already exist.

---

# Mining

After a valid transaction is created, it can be included in a block.

The miner searches for a valid nonce.

For example:

```text
Nonce: 0
Hash: a8f3...

Nonce: 1
Hash: 93bc...

Nonce: 2
Hash: 0000...

Valid block found!
```

The block is then added to the blockchain.

---

# Proof-of-Work

PYC uses a simple Proof-of-Work mechanism.

The block hash must satisfy:

```text
0000xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

The number of required zeros is controlled by the blockchain difficulty.

For example:

```python
DIFFICULTY = 4
```

means the block hash must start with:

```text
0000
```

Increasing the difficulty makes mining computationally more expensive.

---

# Invoice System

PYC includes a basic invoice system.

To create an invoice:

```text
5. Create Invoice
```

You can provide:

```text
Customer wallet
Amount
Description
```

Example:

```text
Customer: PYCabc123...
Amount: 25.00
Description: Website Development
```

The system generates an invoice ID.

Example:

```text
Invoice ID:
INV-20260903-001
```

Invoice information is also stored locally.

---

# Invoice Files

Generated invoices are stored inside:

```text
invoices/
```

Example:

```text
invoices/
├── INV-20260903-001.txt
├── INV-20260903-002.txt
└── INV-20260903-003.txt
```

---

# Invoice Payment

An invoice can be associated with a PYC transaction.

A typical flow is:

```text
Merchant
   │
   │ Creates Invoice
   ▼
Invoice
   │
   │ Customer receives invoice
   ▼
Customer
   │
   │ Sends PYC
   ▼
Blockchain Transaction
   │
   ▼
Invoice marked PAID
```

---

# Transaction History

Choose:

```text
7. Transaction History
```

The system displays transactions involving your wallet.

Example:

```text
Transaction ID: 8f29...
From: PYCabc...
To: PYCxyz...
Amount: 10.00 PYC
Timestamp: 2026-09-03 17:30
```

---

# Blockchain Verification

Choose:

```text
8. Verify Blockchain
```

The system checks the integrity of the entire chain.

It verifies:

* Block hashes
* Previous block references
* Proof-of-Work
* Transaction signatures
* Transaction validity
* Spending rules

Example:

```text
Verifying blockchain...

Block 0: VALID
Block 1: VALID
Block 2: VALID
Block 3: VALID

Blockchain verification successful.
```

If blockchain data has been modified:

```text
Blockchain verification FAILED.
```

---

# Blockchain Explorer

Choose:

```text
9. Blockchain Explorer
```

The explorer displays blocks and their transactions.

Example:

```text
Block #3
-------------------------------
Hash:
0000abc123...

Previous Hash:
0000def456...

Nonce:
18723

Timestamp:
2026-09-03 ...

Transactions:
2
```

---

# Database

PYC uses SQLite for local persistence.

The database stores information such as:

```text
Users
Invoices
Blocks
```

The database is local to the application.

A typical database file may look like:

```text
pyc.db
```

SQLite is used because it is lightweight and does not require a separate database server.

---

# Security

PYC implements several security mechanisms.

## Password Protection

Passwords are processed using:

```text
PBKDF2-HMAC-SHA256
```

with a unique salt.

---

## Private-Key Encryption

Wallet private keys are encrypted using:

```text
AES-GCM
```

The encryption key is derived from the user's password.

---

## Digital Signatures

Transactions are signed using:

```text
Ed25519
```

The receiver and blockchain system can verify that the transaction was authorized by the holder of the corresponding private key.

---

## Hashing

SHA-256 is used for:

* Block hashes
* Transaction IDs
* Wallet address derivation

---

# Configuration

Configuration values are located in:

```text
config.py
```

Important settings may include:

```python
DIFFICULTY = 4
```

The difficulty controls Proof-of-Work mining.

For educational testing, a lower difficulty can be used.

Example:

```python
DIFFICULTY = 2
```

For demonstration:

```text
00xxxxxxxxxxxxxxxx...
```

For the default configuration:

```text
0000xxxxxxxxxxxxxxxx...
```

> Increasing difficulty can significantly increase mining time.

---

# Development Setup

For development:

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run:

```powershell
python main.py
```

---

# Deactivating the Virtual Environment

When finished working:

```powershell
deactivate
```

Your terminal will change from:

```text
(venv) PS A:\projects\FYP IDEAS\PyC\pycproject>
```

to:

```text
PS A:\projects\FYP IDEAS\PyC\pycproject>
```

The virtual environment is **not deleted**.

---

# Activating the Environment Again

Open the project folder:

```powershell
cd "A:\projects\FYP IDEAS\PyC\pycproject"
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

Then run:

```powershell
python main.py
```

---

# Removing the Virtual Environment

If you want to completely recreate the environment:

```powershell
deactivate
```

Then delete:

```text
venv/
```

Create it again:

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

---

# 🛠️ Useful Commands

## Check Python

```powershell
python --version
```

## Check pip

```powershell
python -m pip --version
```

## Check active Python executable

```powershell
python -c "import sys; print(sys.executable)"
```

The result should point to your virtual environment:

```text
...\pycproject\venv\Scripts\python.exe
```

## Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Install cryptography manually

```powershell
python -m pip install cryptography
```

## Check cryptography

```powershell
python -c "import cryptography; print(cryptography.__version__)"
```

## Run application

```powershell
python main.py
```

---

# Troubleshooting

## `ModuleNotFoundError: No module named 'cryptography'`

Run:

```powershell
python -m pip install cryptography
```

Or:

```powershell
python -m pip install -r requirements.txt
```

Then test:

```powershell
python -c "import cryptography; print('Cryptography OK')"
```

---

## Python is not recognized

Check:

```powershell
python --version
```

If Python is not installed, install Python and ensure the Python executable is added to PATH.

---

## Virtual environment does not activate

Try:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell reports an execution-policy error, check the current policy:

```powershell
Get-ExecutionPolicy
```

For development environments, the execution policy may need to permit locally created scripts.

---

## Wrong pip environment

Run:

```powershell
python -c "import sys; print(sys.executable)"
```

and:

```powershell
python -m pip --version
```

Both should point to the same virtual environment.

---

## Mining takes too long

Reduce the difficulty in:

```text
config.py
```

For example:

```python
DIFFICULTY = 2
```

instead of:

```python
DIFFICULTY = 4
```

Higher difficulty means more Proof-of-Work calculations.

---

# Limitations

This project is intentionally an **educational blockchain prototype**.

It is **not a production cryptocurrency**.

The current implementation does not provide:

* Peer-to-peer networking
* Multiple blockchain nodes
* Distributed consensus
* Fork resolution
* Network synchronization
* Decentralized mining
* Production-grade key management
* Hardware wallet support
* Mainnet deployment
* Cryptocurrency exchange integration
* Real-world monetary value
* Protection against all possible attacks

The local blockchain should therefore not be considered equivalent to Bitcoin, Ethereum, or another production cryptocurrency network.

---

# Future Improvements

Possible future versions could introduce:

## P2P Network

Allow multiple PYC nodes to communicate:

```text
Node A ←→ Node B
  ↕         ↕
Node C ←→ Node D
```

---

## Distributed Consensus

Implement a consensus mechanism allowing nodes to agree on the valid blockchain.

Possible approaches:

* Proof-of-Work
* Proof-of-Stake
* Proof-of-Authority

---

## Network Synchronization

Nodes could automatically:

* Discover peers
* Share transactions
* Share blocks
* Synchronize chains
* Resolve forks

---

## Wallet Backup

Add:

* Wallet export
* Wallet import
* Recovery phrase
* Encrypted wallet backup

---

## Web Interface

Build a frontend using:

* React
* Tailwind CSS
* REST API / FastAPI

---

## Blockchain Dashboard

Add:

* Block explorer
* Transaction explorer
* Wallet explorer
* Mining statistics
* Network statistics

---

## Advanced Invoices

Add:

* PDF invoices
* QR codes
* Payment links
* Invoice expiration
* Automatic payment detection
* Merchant dashboard

---

## Additional Security

Future versions could implement:

* Hardware wallet support
* Multi-signature wallets
* Transaction nonces
* Replay protection
* Rate limiting
* Secure key storage
* Network-level authentication

---

# 🎓 Educational Purpose

This project is intended for educational use.

It demonstrates the relationship between:

```text
Cryptography
      ↓
Wallet
      ↓
Transaction
      ↓
Digital Signature
      ↓
Block
      ↓
Proof-of-Work
      ↓
Blockchain
      ↓
Verification
```

The project can be used to understand concepts in:

* Blockchain
* Cryptography
* Cybersecurity
* Distributed systems
* Database systems
* Python programming
* Digital signatures
* Authentication
* Financial technology

---

# Example Transaction Flow

A complete PYC payment can be represented as:

```text
             USER A
               │
               │
          Unlock Wallet
               │
               ▼
        Create Transaction
               │
               ▼
       Sign with Private Key
               │
               ▼
       Verify Digital Signature
               │
               ▼
        Check Wallet Balance
               │
               ▼
          Create Block
               │
               ▼
        Proof-of-Work Mining
               │
               ▼
         Add Block to Chain
               │
               ▼
             USER B
               │
               ▼
          Receives PYC
```

---

# Core Blockchain Concept

Each block contains a reference to the previous block.

```text
┌───────────────┐
│   Genesis     │
│   Block #0    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   Block #1    │
│ Prev Hash ────┼────► Genesis Hash
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   Block #2    │
│ Prev Hash ────┼────► Block #1 Hash
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   Block #3    │
│ Prev Hash ────┼────► Block #2 Hash
└───────────────┘
```

Changing an earlier block changes its hash and breaks the chain relationship.

---

# Dependencies

The primary external dependency is:

```text
cryptography
```

Install all dependencies using:

```powershell
python -m pip install -r requirements.txt
```

---

# Example `requirements.txt`

The project currently uses:

```text
cryptography>=45.0.0
```

---

# Typical Daily Workflow

When continuing development:

```powershell
cd "A:\projects\FYP IDEAS\PyC\pycproject"
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install/update dependencies if required:

```powershell
python -m pip install -r requirements.txt
```

Run:

```powershell
python main.py
```

When finished:

```powershell
deactivate
```

---

# Disclaimer

PYC Blockchain is an educational software project.

PYC does not represent real-world currency and should not be used for real financial transactions.

Do not use this implementation to store real funds, private keys, passwords, or sensitive financial information without significant additional security engineering and independent review.

---

# License

This project is intended for educational and research purposes.

You may modify and extend the project for learning and development.

If this project is used in an academic submission, clearly identify the original author and any third-party libraries or code used.

---

# Author

**Aaryan Koirala**

PYC Blockchain — Educational Cryptocurrency & Blockchain System

---

##  Project Status

```text
Version: 1.0
Status: Educational Prototype
Platform: Python CLI
Blockchain: Local / Single Node
Consensus: Proof-of-Work
Cryptography: Ed25519 + AES-GCM
Database: SQLite
```

---

**PYC — Learn Blockchain by Building One.** 🪙
# pyc---an-educational-purpose
