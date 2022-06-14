from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Callable, Dict, List, Union

from networkx import DiGraph, dfs_postorder_nodes
from tax.core.transactions import Transaction


class TransactionGraph(DiGraph, ABC):
    def __init__(
        self,
        transactions: Union[List[Transaction], Transaction] = [],
    ) -> None:
        if not isinstance(transactions, Iterable):
            transactions = [transactions]

        transactions = self._map_transactions(transactions)

        super().__init__(transactions)

    def _map_transactions(
        self, transactions: List[Transaction]
    ) -> Dict[Transaction, List[Transaction]]:
        return {tx: tx.linked_transactions for tx in transactions}

    @abstractmethod
    def get_transactions(self) -> List[Transaction]:
        raise NotImplementedError


class PostOrderTransactionGraph(TransactionGraph):
    def get_transactions(
        self, filters: Union[List[Callable[..., bool]], Callable[..., bool]] = []
    ) -> List[Transaction]:
        # returns filtered, postorder (linked_transactions) before given transaction
        # i.e. {1: [2, 3], 4: [5, 6]} => [2, 3, 1, 5, 6, 4]

        tx_list = [tx for tx in dfs_postorder_nodes(self)]

        if not isinstance(filters, Iterable):
            filters = [filters]

        if len(filters) == 0:
            # return without filters
            return tx_list

        for fltr in filters:
            filtered_txs = filter(fltr, tx_list)

        return list(filtered_txs)
