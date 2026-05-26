from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from hashlib import sha256
from typing import Any
from urllib.parse import quote_plus


@dataclass(frozen=True)
class EcpayConfig:
    checkout_url: str
    merchant_id: str
    hash_key: str
    hash_iv: str


def _ecpay_url_encode(value: str) -> str:
    encoded = quote_plus(value, safe='').lower()
    replacements = {
        '%2d': '-',
        '%5f': '_',
        '%2e': '.',
        '%21': '!',
        '%2a': '*',
        '%28': '(',
        '%29': ')',
    }
    for source, target in replacements.items():
        encoded = encoded.replace(source, target)
    return encoded


def generate_check_mac_value(params: dict[str, Any], *, hash_key: str, hash_iv: str) -> str:
    filtered = {
        key: '' if value is None else str(value)
        for key, value in params.items()
        if key != 'CheckMacValue'
    }
    sorted_pairs = sorted(filtered.items(), key=lambda item: item[0].lower())
    raw = '&'.join([f'HashKey={hash_key}', *[f'{key}={value}' for key, value in sorted_pairs], f'HashIV={hash_iv}'])
    encoded = _ecpay_url_encode(raw)
    return sha256(encoded.encode('utf-8')).hexdigest().upper()


def verify_check_mac_value(params: dict[str, Any], *, hash_key: str, hash_iv: str) -> bool:
    received = str(params.get('CheckMacValue', '')).upper()
    if not received:
        return False
    expected = generate_check_mac_value(params, hash_key=hash_key, hash_iv=hash_iv)
    return received == expected


def build_checkout_params(
    *,
    merchant_id: str,
    order_number: str,
    total_amount: Decimal,
    item_names: list[str],
    return_url: str,
    client_back_url: str | None = None,
) -> dict[str, str]:
    rounded_total = int(total_amount.quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    display_items = [name.replace('#', ' ') for name in item_names] or ['毛孩樂園商品']
    params = {
        'MerchantID': merchant_id,
        'MerchantTradeNo': order_number,
        'MerchantTradeDate': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'PaymentType': 'aio',
        'TotalAmount': str(max(rounded_total, 1)),
        'TradeDesc': '毛孩樂園訂單',
        'ItemName': '#'.join(display_items)[:400],
        'ReturnURL': return_url,
        'ChoosePayment': 'ALL',
        'EncryptType': '1',
    }
    if client_back_url:
        params['ClientBackURL'] = client_back_url
    return params


def parse_payment_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y/%m/%d %H:%M:%S')
    except ValueError:
        return None
