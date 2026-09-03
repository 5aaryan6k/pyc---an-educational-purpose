from pathlib import Path


def generate_invoice(
    invoice_id,
    sender,
    receiver,
    amount,
    description,
    status,
    created_at,
):

    directory = Path(
        "invoices"
    )

    directory.mkdir(
        exist_ok=True
    )

    filename = (
        directory
        / f"{invoice_id}.txt"
    )

    content = f"""
============================================================
                         PYC INVOICE
============================================================

Invoice ID:
{invoice_id}

Status:
{status}

Created:
{created_at}

------------------------------------------------------------

FROM WALLET:
{sender}

TO WALLET:
{receiver}

AMOUNT:
{amount} PYC

DESCRIPTION:
{description}

------------------------------------------------------------

Payment instructions:

Send exactly:

{amount} PYC

to:

{receiver}

============================================================
                    PYC BLOCKCHAIN
============================================================
"""

    filename.write_text(
        content.strip(),
        encoding="utf-8",
    )

    return filename