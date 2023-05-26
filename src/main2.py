import csv
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List

from cryptax.fills import Fill

txs_file = "/workspaces/ten-second-tools/src/tax/data/fills_CoinbasePro_2021.csv"


@dataclass
class FillReportRecord:
    portfolio: str
    trade_id: int
    product: str
    side: str
    created_at: datetime
    size: float
    size_unit: str
    price: float
    fee: float
    total: float
    price_fee_total_unit: str


class CoinbaseProFillFactory:
    def get_transactions(self, transaction_report_file_path: str) -> List[Fill]:
        fill_records = self._read_fill_report(transaction_report_file_path)
        transactions = [self._build_fill(r) for r in fill_records]

        return transactions

    def _build_fill(self, record: FillReportRecord) -> Fill:
        # TODO get_usd_price_at_timestamp(record.time)
        usd_price = 1.23

        return Fill(
            record.created_at,
            record.side,
            record.portfolio,
            record.trade_id,
            record.size_unit,
            record.size,
            record.price_fee_total_unit,
            record.price,
            record.fee,
            record.total,
        )

    def _read_fill_report(
        self, file_path: str, header: bool = True
    ) -> List[FillReportRecord]:
        # reading fill report file *and* managing cast to proper types
        cast_types = [i for i in FillReportRecord.__annotations__.values()]

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

                transactions.append(FillReportRecord(*data_cast))

        return transactions


cbpff = CoinbaseProFillFactory()
txs = cbpff.get_transactions(txs_file)

usd_filter_txs = [tx for tx in txs if tx.basis_product == "USD"]

sells = [tx for tx in usd_filter_txs if tx.side == "SELL"]
buys = [tx for tx in usd_filter_txs if tx.side == "BUY"]

gain_txs = []

for sell in sells:
    avail_buys = [
        b for b in buys if b.product == sell.product and b._filled_size < b.size
    ]
    for buy in avail_buys:
        if sell._filled_size < sell.size:
            tx = buy.fill(sell)
            gain_txs.append(tx)
    if sell._filled_size < sell.size:
        empty_fill = Fill.fulfills(sell)
        tx = empty_fill.fill(sell)
        gain_txs.append(tx)

[print(g) for g in gain_txs]
print("\ntotal_txs:", len(gain_txs))

gain = 0
for g in gain_txs:
    gain += g.proceeds - g.cost_basis

print("gain:", gain)


def write_dataclass_array_to_csv(
    array: List[dataclass], filepath: str, header: bool = True
) -> None:
    fields = asdict(array[0]).keys()
    data = [asdict(item).values() for item in array]

    with open(filepath, "w+") as file:
        writer = csv.writer(file)

        if header:
            writer.writerow(fields)
        writer.writerows(data)


write_dataclass_array_to_csv(gain_txs, "test.csv")
