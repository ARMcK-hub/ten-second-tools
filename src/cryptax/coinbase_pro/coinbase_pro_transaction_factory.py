import csv
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Type

from cryptax.core.transactions import (
    Acquisition,
    Deposit,
    Distribution,
    Fee,
    Transaction,
    TransactionFactory,
    Withdrawl,
)


@dataclass
class TransactionReportRecord:
    portfolio: str
    type: str
    time: datetime
    amount: float
    balance: float
    amount_balance_unit: str
    transfer_id: str
    trade_id: int
    order_id: str


class UndefinedTransactionError(Exception):
    def __init__(self, record: TransactionReportRecord) -> None:
        message = f"Unable to map to Transaction: {record.type}"
        super().__init__(message)


class CoinbaseProTransactionFactory(TransactionFactory):
    def get_transactions(self, transaction_report_file_path: str) -> Transaction:
        transaction_records = self._read_account_report(transaction_report_file_path)
        transactions = [self._build_transaction(r) for r in transaction_records]

        # linking transactions
        linked_transactions = self._link_transactions(transactions)

        return linked_transactions

    def _link_transactions(self, transactions: List[Transaction]) -> List[Transaction]:
        for tx in transactions:
            # link all transactions with same id, except itself
            tx.linked_transactions = [
                t for t in transactions if t.id == tx.id and t != tx
            ]

        return transactions

    def _build_transaction(self, record: TransactionReportRecord) -> Transaction:
        __coinbase_transaction_map = {
            "deposit": Deposit,
            "withdrawal": Withdrawl,
            "fee": Fee,
        }
        tx_type: Optional[Type[Transaction]] = None

        if record.type in __coinbase_transaction_map.keys():
            tx_type = __coinbase_transaction_map.get(record.type)
            tx_id = record.transfer_id if record.transfer_id != "" else record.order_id

        if record.type in ("match", "conversion"):
            tx_type = Acquisition if record.amount >= 0 else Distribution
            tx_id = record.order_id

        if tx_type is None:
            raise UndefinedTransactionError(record)

        # TODO get_usd_price_at_timestamp(record.time)
        usd_price = 1.23

        return tx_type(
            tx_id,
            record.time,
            record.amount_balance_unit,
            abs(record.amount),
            usd_price,
            usd_price * abs(record.amount),
            [],
            0,
            [],
        )

    def _read_account_report(
        self, file_path: str, header: bool = True
    ) -> List[TransactionReportRecord]:
        # reading account report file *and* managing cast to proper types
        cast_types = [i for i in TransactionReportRecord.__annotations__.values()]

        with open(file_path, "r") as file:
            reader = csv.reader(file)
            transactions = []

            for index, row in enumerate(reader):
                if index == 0 and header:
                    continue

                data_cast = []

                for index, value in enumerate(row):
                    if cast_types[index] == datetime:
                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
                    elif value != "":
                        value = cast_types[index](value)
                    data_cast.append(value)

                transactions.append(TransactionReportRecord(*data_cast))

        return transactions
