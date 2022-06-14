from datetime import datetime
from typing import Type

import pytest
from tax.core.transactions import (
    Acquisition,
    Deposit,
    Distribution,
    Fee,
    OverRecognizedTransactionError,
    SelfFulfillmentTransactionError,
    Transaction,
    Withdrawl,
)


def build_test_transaction(
    tx_type: Type[Transaction], high: bool = False
) -> Transaction:
    amount = 1.1 if high else 1.0
    asset_price_usd = 2.0

    return tx_type(
        "test_id",
        datetime.now(),
        "test_asset",
        amount,
        asset_price_usd,
        abs(amount * asset_price_usd),
        [],
        0,
        [],
    )


TRANSACTION_TYPES = [Deposit, Distribution, Acquisition, Fee, Withdrawl]


def test_cannot_create() -> None:
    with pytest.raises(TypeError):
        Transaction()


def test_can_create() -> None:
    for type in TRANSACTION_TYPES:
        build_test_transaction(type)


def test_can_hash() -> None:
    for type in TRANSACTION_TYPES:
        hash(build_test_transaction(type))


def test_can_recognize_allowable_amount() -> None:
    recognizing_amount = 1
    tx = build_test_transaction(Distribution)
    tx.recognize(recognizing_amount)

    assert tx.amount_recognized == recognizing_amount


def test_raises_on_over_recognized_amount() -> None:
    tx = build_test_transaction(Distribution)

    with pytest.raises(OverRecognizedTransactionError):
        tx.recognize(tx.amount + 1)


def test_transactions_can_fulfill_eachother() -> None:
    tx_a = build_test_transaction(Acquisition)
    tx_b = build_test_transaction(Distribution)

    tx_b.fulfill_transaction(tx_a)

    # both recognized amounts
    assert all([tx_a.amount_recognized > 0, tx_b.amount_recognized > 0])

    # both associated themselves
    assert all(
        [tx_a in tx_b.fulfillment_transactions, tx_b in tx_a.fulfillment_transactions]
    )


def test_differing_transactions_can_fullfill() -> None:
    tx_a = build_test_transaction(Acquisition, True)
    tx_b = build_test_transaction(Distribution)

    tx_b.fulfill_transaction(tx_a)
    tx_a.fulfill_transaction(tx_b)


def test_transactions_fullfill_minimum_amount() -> None:
    tx_a = build_test_transaction(Acquisition, True)
    tx_b = build_test_transaction(Distribution)

    tx_b.fulfill_transaction(tx_a)

    assert all(
        [tx_a.amount_recognized == tx_b.amount, tx_b.amount_recognized == tx_b.amount]
    )


def test_transaction_cannot_fulfill_self() -> None:
    tx = build_test_transaction(Distribution)

    with pytest.raises(SelfFulfillmentTransactionError):
        tx.fulfill_transaction(tx)
