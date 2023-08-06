from dataclasses import dataclass


@dataclass
class Receiver:
    name: str
    phone: str

    def __str__(self):
        return f"{self.name} {self.phone} "
