from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class GainTransaction:
    product: str
    purchase_date: datetime
    cost_basis: float
    date_sold: datetime
    proceeds: float


class OverRecognizedTransactionError(Exception):
    def __init__(
        self,
        overrecognized_transaction: Fill,
        recognizing_amount: float,
    ) -> None:

        message = f"""Unable to recognize transaction {overrecognized_transaction.trade_id}.
        Attempted to recognize {recognizing_amount} with current {overrecognized_transaction._filled_size} recognized and max {overrecognized_transaction.size}."""
        super().__init__(message)


class SelfFulfillmentTransactionError(Exception):
    def __init__(self, transaction: Fill) -> None:
        message = f"Transaction of id {transaction.trade_id} cannot fulfill self."
        super().__init__(message)


@dataclass
class Fill:
    created_at: datetime
    side: str
    portfolio: str
    trade_id: int
    product: str  # size_unit
    size: float
    basis_product: str  # price_fee_total_unit
    price: float
    fee: float
    total: float
    _filled_size: float = 0

    @property
    def _unrecognized_size(self) -> float:
        return self.size - self._filled_size

    def fill(self, target_fill: Fill) -> GainTransaction:
        # fulfills a transactions recognizable amount with the maximum allowed
        if target_fill == self:
            raise SelfFulfillmentTransactionError(self)

        minimum_recognizable_amount = min(
            [self._unrecognized_size, target_fill._unrecognized_size]
        )

        if minimum_recognizable_amount > 0:
            self.recognize(minimum_recognizable_amount)
            target_fill.recognize(minimum_recognizable_amount)

        return GainTransaction(
            target_fill.product,
            self.created_at,
            minimum_recognizable_amount * self.price,
            target_fill.created_at,
            minimum_recognizable_amount * target_fill.price,
        )

    def recognize(self, recognizing_amount: float) -> None:
        # recognizes a given amount
        if self._filled_size + recognizing_amount > self.size:
            raise OverRecognizedTransactionError(self, recognizing_amount)

        self._filled_size += recognizing_amount

    @classmethod
    def fulfills(cls, target_fill: Fill) -> Fill:
        return Fill(
            target_fill.created_at,
            "AUTOGENERATE",
            target_fill.portfolio,
            0,
            target_fill.product,
            target_fill.size - target_fill._filled_size,
            target_fill.basis_product,
            0,
            0,
            0,
            0,
        )
