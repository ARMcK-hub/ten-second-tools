from datetime import datetime
from typing import Type

import pytest
from tax.core.transactions import (
    Distribution,
    PostOrderTransactionGraph,
    Transaction,
    TransactionGraph,
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


def test_cannot_create() -> None:
    with pytest.raises(TypeError):
        TransactionGraph()


def test_can_create() -> None:
    PostOrderTransactionGraph()


def test_can_build_with_transactions() -> None:
    txs = [build_test_transaction(Distribution) for i in range(5)]

    PostOrderTransactionGraph(txs)


def test_can_get_transactions() -> None:
    txs = [build_test_transaction(Distribution) for i in range(5)]

    g = PostOrderTransactionGraph(txs)

    g.get_transactions()


def test_transactions_persist_after_sorting() -> None:
    txs = [build_test_transaction(Distribution) for i in range(5)]
    init_txs = set(txs)

    g = PostOrderTransactionGraph(txs)

    g_txs = g.get_transactions()
    sort_txs = set(g_txs)

    assert sort_txs == init_txs


def test_linked_transactions_persist_after_sorting() -> None:
    txs = [build_test_transaction(Distribution) for i in range(5)]
    valid_txs = txs.copy()

    for tx in txs:
        link_tx = build_test_transaction(Distribution)
        tx.linked_transactions.append(link_tx)
        valid_txs.append(link_tx)

    g = PostOrderTransactionGraph(txs)

    g_txs = g.get_transactions()
    # f = g_txs.

    assert txs.sort(key=id) == g_txs.sort(key=id)


def test_can_filter_transactions() -> None:
    high_tx_count = 2
    high_txs = [
        build_test_transaction(Distribution, True) for i in range(high_tx_count)
    ]

    txs = [build_test_transaction(Distribution) for i in range(2)]

    txs.extend(high_txs)
    g = PostOrderTransactionGraph(txs)

    def amount_filter(transaction: Transaction) -> bool:
        return transaction.amount > 1

    filtered_txs = g.get_transactions(amount_filter)

    assert len(filtered_txs) == high_tx_count
