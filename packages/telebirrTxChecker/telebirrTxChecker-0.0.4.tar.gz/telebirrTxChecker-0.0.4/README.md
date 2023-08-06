# Telebirr Transaction Checker/Parser

This is a simple script that checks your Telebirr transactions and parses them 

### ⚠️ Not finished yet

## Installation

```bash
pip install git+https://github.com/wizkiye/telebirr-tx-checker.git
```

## Usage

```python
from ttxc import TelebirrTxChecker


async def main():
    checker = TelebirrTxChecker()
    tx = await checker.get_transaction("<TRANSACTION_ID>")
    print(tx.status)
    print(tx.id)
    print(tx.total_sent)
    print(tx.total_amount_in_word)
    print(tx.mode)
    print(tx.channel)
    print(tx.payer)
    print(tx.payer.name)
    print(tx.payer.phone)
    print(tx.payer.account_type)
    ...

```

## License
[MIT](https://choosealicense.com/licenses/mit/)
```

