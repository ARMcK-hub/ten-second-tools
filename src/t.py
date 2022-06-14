# from datetime import datetime, timedelta

# from dateutil.relativedelta import relativedelta

# now = datetime.now()
# st = datetime.fromtimestamp(1641016800)
# lt = datetime.fromtimestamp(1577858400)


# stv = now - relativedelta(years=1)
# st = now.replace(day=1)
# lt = now.replace(year=now.year - 1, day=now.day - 1)
# print(st > stv)

# t = (1, 2, 3, 4, 5)
# l = []
# l.extend([i for i in t if i != t[1]])
# print(l)


# import csv

# from dataclasses import asdict, dataclass
# from typing import Any, Dict, List


# @dataclass
# class Fill:
#     size: float
#     to_product: str
#     from_product: str
#     total_usd_price: float


# text = [Fill(1.1, "BTC", "REN", 123.2), Fill(1.3, "REN", "USD", 110)]
# rows = [asdict(t) for t in text]


# def write(filepath: str, rows: List[Dict[str, Any]]) -> None:
#     header = rows[0].keys()
#     unpacked_rows = [d.values() for d in rows]

#     data = [header, *unpacked_rows]

#     with open(filepath, mode="w+", newline="") as file:
#         writer = csv.writer(file)
#         writer.writerows(data)


# write("test.csv", rows)
