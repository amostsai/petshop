from decimal import Decimal

from app.features.cart.ecpay import (
    build_checkout_params,
    generate_check_mac_value,
    verify_check_mac_value,
)


def test_build_checkout_params_uses_stage_order_fields():
    params = build_checkout_params(
        merchant_id="3002607",
        order_number="PS250101000000",
        total_amount=Decimal("840.00"),
        item_names=["有機鮮肉主食餐 (狗)", "逗貓智能球"],
        return_url="https://example.test/cart/ecpay/return",
        client_back_url="https://example.test/cart/thank-you/PS250101000000",
    )

    assert params["MerchantID"] == "3002607"
    assert params["MerchantTradeNo"] == "PS250101000000"
    assert params["TotalAmount"] == "840"
    assert params["PaymentType"] == "aio"
    assert params["ChoosePayment"] == "ALL"
    assert params["EncryptType"] == "1"
    assert params["ItemName"] == "有機鮮肉主食餐 (狗)#逗貓智能球"


def test_check_mac_value_round_trip():
    params = {
        "MerchantID": "3002607",
        "MerchantTradeNo": "PS250101000000",
        "MerchantTradeDate": "2025/01/01 12:00:00",
        "PaymentType": "aio",
        "TotalAmount": "840",
        "TradeDesc": "毛孩樂園訂單",
        "ItemName": "有機鮮肉主食餐 (狗)",
        "ReturnURL": "https://example.test/cart/ecpay/return",
        "ChoosePayment": "ALL",
        "EncryptType": "1",
    }
    check_mac_value = generate_check_mac_value(
        params,
        hash_key="pwFHCqoQZGmho4w6",
        hash_iv="EkRm7iFT261dpevs",
    )

    assert len(check_mac_value) == 64
    assert check_mac_value == check_mac_value.upper()

    signed_params = {**params, "CheckMacValue": check_mac_value}
    assert verify_check_mac_value(
        signed_params,
        hash_key="pwFHCqoQZGmho4w6",
        hash_iv="EkRm7iFT261dpevs",
    )
