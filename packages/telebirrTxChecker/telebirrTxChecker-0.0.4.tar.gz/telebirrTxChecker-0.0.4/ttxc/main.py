from datetime import datetime
from typing import Union, Optional

import httpx
import pdfkit

from ttxc import constants, utils
from ttxc.errors import TransactionNotFound
from ttxc.types import Transaction, Payer, Receiver


def r_birr(text: str):
    return float(text.strip(" Birr"))


class TelebirrTxChecker:
    def __init__(
        self,
        proxies: Optional[dict] = None,
    ):
        self.s = httpx.AsyncClient(
            proxies=proxies,
            headers=constants.HEADERS,
            timeout=constants.TIMEOUT,
            verify=False,
        )

    async def process_request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Union[str, dict] = None,
    ):
        res = await self.s.request(
            method, constants.BASE_URL.format(endpoint), data=data
        )
        return res.text

    async def get_transaction(self, transaction_id: str):
        res = await self.process_request(transaction_id)
        data = utils.parse_transaction(res)
        if data is None:
            raise TransactionNotFound(f"Transaction with id {transaction_id} not found")
        return Transaction(
            id=transaction_id,
            payer=Payer(
                name=data["payer_name"],
                phone=data["payer_phone"],
                account_type=data["payer_account_type"],
            ),
            receiver=Receiver(
                name=data["receiver_name"],
                phone=data["receiver_phone"],
            ),
            status=data["status"],
            discount=r_birr(data["discount"]),
            vat=r_birr(data["vat"]),
            total_amount_in_word=data["total_amount_in_word"],
            total_sent=r_birr(data["total_sent"]),
            date=datetime.strptime(data["date"], "%d-%m-%Y %H:%M:%S"),
            mode=data["mode"],
            reason=data["reason"],
            channel=data["channel"],
            base=self,
        )

    @staticmethod
    async def save_pdf(tx_id: str, path: str) -> bool:
        return pdfkit.from_url(constants.BASE_URL.format(tx_id), path)
