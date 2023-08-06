from dataclasses import dataclass


@dataclass
class Payer:
    name: str
    phone: str
    account_type: str

    def __str__(self):
        return f"{self.name} {self.phone} {self.account_type}"
