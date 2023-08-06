from dataclasses import dataclass
from datetime import datetime

import ttxc
from ttxc.types import Payer
from ttxc.types import Receiver
from ttxc.utils import format_phone


@dataclass
class Transaction:
    id: str
    payer: Payer
    receiver: Receiver
    status: str
    discount: float
    vat: float
    total_amount_in_word: str
    total_sent: float
    date: datetime
    mode: str
    reason: str
    channel: str
    base: "ttxc.TelebirrTxChecker"

    def __str__(self):
        return f"{self.id} {self.payer} {self.receiver} {self.status} {self.discount} {self.vat} {self.total_amount_in_word} {self.total_sent} {self.date} {self.amount} {self.mode} {self.reason} {self.channel}"

    def is_mine(self, phone: str = None, name: str = None):
        if phone is None and name is None:
            raise ValueError("phone or name must be set")
        return (
            format_phone(self.receiver.phone) == format_phone(phone)
            and self.receiver.name.lower() == name.lower()
        )

    @property
    def is_paid(self):
        return self.status.lower() == "completed"

    async def save_pdf(self, path: str) -> bool:
        return await self.base.save_pdf(self.id, path)

    def dict(self):
        return {
            "id": self.id,
            "payer": self.payer.__dict__,
            "receiver": self.receiver.__dict__,
            "status": self.status,
            "discount": self.discount,
            "vat": self.vat,
            "total_amount_in_word": self.total_amount_in_word,
            "total_sent": self.total_sent,
            "date": self.date.isoformat(),
            "mode": self.mode,
            "reason": self.reason,
            "channel": self.channel,
        }
