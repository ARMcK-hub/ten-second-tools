from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


class OverRecognizedTransactionError(Exception):
    def __init__(
        self,
        overrecognized_transaction: Transaction,
        recognizing_amount: float,
    ) -> None:

        message = f"""Unable to recognize transaction {overrecognized_transaction.id}.
        Attempted to recognize {recognizing_amount} with current {overrecognized_transaction.amount_recognized} recognized and max {overrecognized_transaction.amount}."""
        super().__init__(message)


class SelfFulfillmentTransactionError(Exception):
    def __init__(self, transaction: Transaction) -> None:
        message = f"Transaction of id {transaction.id} cannot fulfill self."
        super().__init__(message)


@dataclass
class Transaction(ABC):
    id: str
    time: Optional[datetime]
    asset: str
    amount: float  # <0: sell; >0: buy
    asset_price_usd: float
    amount_usd: float
    # transactions that are associated by id (i.e. same order)
    linked_transactions: List[Transaction]
    # placeholder for recognized size of transaction, fulfilled by fulfillment transactions
    amount_recognized: str
    # transactions that fulfill the recognizable amount
    fulfillment_transactions: List[Transaction]

    @property
    @abstractmethod
    def is_taxable(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __hash__(self) -> int:
        # required for DAG integration
        raise NotImplementedError

    @property
    def unrecognized_size(self) -> float:
        return self.amount - self.amount_recognized

    def fulfill_transaction(self, transaction: Transaction) -> None:
        # fulfills a transactions recognizable amount with the maximum allowed
        if transaction == self:
            raise SelfFulfillmentTransactionError(self)

        minimum_recognizable_amount = min(
            [self.unrecognized_size, transaction.unrecognized_size]
        )

        if minimum_recognizable_amount > 0:
            self.recognize(minimum_recognizable_amount)
            transaction.recognize(minimum_recognizable_amount)

            self.fulfillment_transactions.append(transaction)
            transaction.fulfillment_transactions.append(self)

    def recognize(self, recognizing_amount: float) -> None:
        # recognizes a given amount
        if self.amount_recognized + recognizing_amount > self.amount:
            raise OverRecognizedTransactionError(self, recognizing_amount)

        self.amount_recognized += recognizing_amount


@dataclass
class Distribution(Transaction):
    @property
    def is_taxable(self) -> bool:
        return False if self.asset == "USD" else True

    def __hash__(self) -> int:
        # required for DAG integration
        return hash(repr(self))


@dataclass
class Acquisition(Transaction):
    @property
    def is_taxable(self) -> bool:
        return False

    def __hash__(self) -> int:
        # required for DAG integration
        return hash(repr(self))


@dataclass
class Fee(Distribution):
    @property
    def is_taxable(self) -> bool:
        return False

    def __hash__(self) -> int:
        # required for DAG integration
        return hash(repr(self))


@dataclass
class Withdrawl(Distribution):
    """
    Type of Distribution that removes equity from interacting platform.
    """

    def __hash__(self) -> int:
        # required for DAG integration
        return hash(repr(self))

    @property
    def is_taxable(self) -> bool:
        # this becomes taxable if it is no longer if you
        if hasattr(self, "_is_taxable"):
            return self._is_taxable
        return False

    @is_taxable.setter
    def is_taxable(self, taxable: bool = True) -> None:
        self._is_taxable = taxable


@dataclass
class Deposit(Acquisition):
    """
    Type of Acquisition that adds equity to interacting platform.
    """

    def __hash__(self) -> int:
        # required for DAG integration
        return hash(repr(self))

    @property
    def is_taxable(self) -> bool:
        return False
