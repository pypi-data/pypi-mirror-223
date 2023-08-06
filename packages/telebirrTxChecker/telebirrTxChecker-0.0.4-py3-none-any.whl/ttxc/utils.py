import re

from bs4 import BeautifulSoup


def parse_transaction(html: str):
    soup = BeautifulSoup(html, "lxml")
    try:
        payer_name = find_next("""የከፋይ ስም/Payer Name""", soup)
        payer_phone = find_next("""የከፋይ ቴሌብር ቁ./Payer telebirr no.""", soup)
        transaction_status = find_next("""የክፍያው ሁኔታ/transaction status""", soup)
        receiver_name = find_next("""የገንዘብ ተቀባይ ስም/Credited Party name""", soup)
        receiver_phone = find_next("""የገንዘብ ተቀባይ ቴሌብር ቁ./Credited party""", soup)
        payer_account_type = find_next("""የከፋይ አካውንት አይነት/Payer account type""", soup)
        discount_amount = find_next("ቅናሽ/Discount Amount", soup)
        vat = find_next("15% ቫት/VAT", soup)
        total_amount_in_word = find_next("የገንዘቡ ልክ በፊደል/Total Amount in word", soup)
        total_sent = find_next("ጠቅላላ የተክፈለ/Total Amount Paid", soup)
        payment_mode = find_next(" የክፍያ ዘዴ/Payment Mode", soup)
        reason = find_next("የክፍያ ምክንያት/Payment Reason", soup)
        channel = find_next("የክፍያ መንገድ/Payment channel", soup)
        date = re.search(r"\d{2}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2}", soup.text).group()
    except AttributeError:
        return None
    return {
        "payer_name": payer_name,
        "payer_phone": payer_phone,
        "status": transaction_status,
        "receiver_name": receiver_name,
        "receiver_phone": receiver_phone,
        "payer_account_type": payer_account_type,
        "discount": discount_amount,
        "vat": vat,
        "total_amount_in_word": total_amount_in_word,
        "total_sent": total_sent,
        "mode": payment_mode,
        "reason": reason,
        "channel": channel,
        "date": date,
    }


def find_next(text: str, soup: BeautifulSoup):
    return soup.find("td", text=re.compile(text)).find_next("td").text.strip()


def format_phone(phone: str):
    if phone.startswith("251"):
        return phone
    if phone.startswith("9"):
        return "251" + phone
    if phone.startswith("0"):
        return "251" + phone[1:]
    return phone
