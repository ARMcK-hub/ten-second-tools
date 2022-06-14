from abc import ABC
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from dateutil.relativedelta import relativedelta
from tax.core.transactions import Transaction
from tax.core.transactions.transaction_graph import PostOrderTransactionGraph


class CostBasisStrategy(ABC):
    """
    Defines how gains or losses should be recognized.
    """

    name: Optional[str] = None

    def __init__(self, config: Dict[str, str]) -> None:
        self._config = config

    def recognize_taxable_transactions(
        self,
        taxable_transactions: List[Transaction],
        unmatched_purchases: List[Transaction],
    ) -> Tuple[List[Transaction], List[Transaction]]:
        """
        Returns a list of matched, recognized fills and
        a lit of remaining, unmatched purchase fills for use at later runtime.
        """
        raise NotImplementedError

    def _get_longterm_date(self, transaction_time: datetime) -> datetime:
        return transaction_time - relativedelta(years=1)

    def get_available_longterm_transactions(
        self, taxable_transaction: Transaction, unmatched_purchases: List[Transaction]
    ) -> List[Transaction]:
        # gets same-asset, longterm qualifying transactions occuring before taxable_transaction
        longterm_validator = self._get_longterm_date(taxable_transaction.time)
        return [
            up
            for up in unmatched_purchases
            if up.time <= longterm_validator
            and up.time <= taxable_transaction.time
            and up.asset == taxable_transaction.asset
            and up.amount_recognized < up.amount
        ]

    def get_available_shortterm_transactions(
        self, taxable_transaction: Transaction, unmatched_purchases: List[Transaction]
    ) -> List[Transaction]:
        # gets same-asset, shortterm qualifying transactions occuring before taxable_transaction
        longterm_validator = self._get_longterm_date(taxable_transaction.time)
        return [
            up
            for up in unmatched_purchases
            if up.time > longterm_validator
            and up.time <= taxable_transaction.time
            and up.asset == taxable_transaction.asset
            and up.amount_recognized < up.amount
        ]

    def evaluate_linked_transactions(self, transaction: Transaction) -> Transaction:
        if len(transaction.linked_transactions) == 0:
            # todo
            return transaction

        return transaction


class FirstInFirstOutCostBasisStrategy(CostBasisStrategy):
    """
    Recognizes the earliest security related fills, unbiased to capital gain.
    """

    name = "first_in_first_out"

    def recognize_taxable_transactions(
        self,
        taxable_transactions: List[Transaction],
        unmatched_purchases: List[Transaction],
    ) -> Tuple[List[Transaction], List[Transaction]]:
        raise NotImplementedError


class LastInFirstOutCostBasisStrategy(CostBasisStrategy):
    """
    Recognizes the latest security related fills, unbiased to capital gain.
    """

    name = "last_in_first_out"

    def recognize_taxable_transactions(
        self,
        taxable_transactions: List[Transaction],
        unmatched_purchases: List[Transaction],
    ) -> Tuple[List[Transaction], List[Transaction]]:
        raise NotImplementedError


class HighestCostBasisStrategy(CostBasisStrategy):
    """
    Recognizes the highest cost basis to reduce capital gains.
    """

    name = "highest"

    def recognize_taxable_transactions(
        self,
        taxable_transactions: List[Transaction],
        unmatched_purchases: List[Transaction],
    ) -> Tuple[List[Transaction], List[Transaction]]:
        raise NotImplementedError


class LowestCostBasisStrategy(CostBasisStrategy):
    """
    Recognizes the lowest cost basis to increase capital gains.
    """

    name = "lowest"

    def recognize_taxable_transactions(
        self,
        taxable_transactions: List[Transaction],
        unmatched_purchases: List[Transaction],
    ) -> Tuple[List[Transaction], List[Transaction]]:
        def is_not_taxable_filter(tx: Transaction) -> bool:
            return not tx.is_taxable

        for tx in taxable_transactions:
            print(f"evaluating {tx.id} with amount {tx.amount}")
            lttx = self.get_available_longterm_transactions(tx, unmatched_purchases)
            sttx = self.get_available_shortterm_transactions(tx, unmatched_purchases)

            prioritized_fulfillment_txs = lttx + sttx
            tx_graph = PostOrderTransactionGraph(prioritized_fulfillment_txs)
            print(len(tx_graph.nodes))
            for ftx in tx_graph.get_transactions(is_not_taxable_filter):
                ftx.fulfill_transaction(tx)
                print(f"filling with {ftx.id} with amount {ftx.amount}")

                if tx.amount_recognized == tx.amount:
                    print(f"filled amount {tx.amount_recognized}")
                    break


class CustomCostBasisStrategy(CostBasisStrategy):
    name = "custom"

    def recognize_taxable_transactions(
        self,
        taxable_transactions: List[Transaction],
        unmatched_purchases: List[Transaction],
    ) -> Tuple[List[Transaction], List[Transaction]]:
        raise NotImplementedError
