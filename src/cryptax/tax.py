from __future__ import annotations

from datetime import datetime
from typing import List, Optional

"""
### Gain / Loss Report:
Currency Name
Purchase Date
Cost Basis (purchase $)
Date Sold
Proceeds (sell $)

### Unrecognized Purchase Fills:
Fill 1, 2, ...

### Taxable Transactions:
Fill 1, 2, ...

### COST BASIS METHODS: (works on specific identification, so average not available)
FIFO - sell earliest bought
LIFO - sell latest bought
High Cost - sell highest cost to reduce gains (do not want to realize gains)
Low Cost - sell lowest cost to realize gains (want to realize gains)
Specific Identification - identify specific purchases for optimization (meet gain target, prefer recognize gains on particular assets)

if __name__ == "__main__":

    cost_basis_strategy = CostBasisStrategyFactory(config.cost_basis_strategy, config.cost_basis_strategy_config).get_strategy()

    fill_manager = FillManager()

    for fill_source, fill_config in config_fill_sources.items():
        fill_factory = FillFactoryProvider(fill_source).get_factory(fill_config)
        unrecognized_purchases = fill_factory.get_unrecognized_fills()
        taxable_transactions = fill_factory.get_taxable_fills()
        fill_manager.add_fills(unrecognized_purchases)
        fill_manager.add_fills(taxable_transactions)


    evaluation = fill_manager.evaluate_to_files(cost_basis_strategy, 'config/path/to/output_dir') # unrecognized purchase fills, turbo_tax gain / loss report, gain / loss summary, full gain / loss report
"""


class Transaction:  # CoinbasePro
    # from account report
    portfolio: str
    type: str
    time: datetime
    amount: float
    balance: float
    amount_balance_unit: str  # to_product
    transfer_id: str
    trade_id: int  # PK join Fill, 1Fill:ManyTxs
    order_id: str


class Fill:  # CoinbasePro
    # from fills report
    portfolio: str
    trade_id: str  # PK join Transaction, 1Fill:ManyTxs
    product: str
    from_product: str
    to_product: str
    side: str
    created_at: datetime
    size: float
    size_unit: str  # from_product
    price: float
    fee: float
    total: float
    price_fee_total_unit: str  # to_product
    _transactions: List[Transaction]  # transactions for this Fill
    # transactions registered to this fill (for sell, these are buy, for buy, these are sell)
    _registered_size: float  # amount already registered under another fill
    _registered_fills: List[Fill]
    _completed_at: Optional[datetime]  # last transaction time
    _usd_price: float


# get all txs
all_txs: List[Transaction] = [Transaction()]
all_fills: List[Fill] = [Fill()]

# get all txs for a given fill
for fill in all_fills:
    fill._transactions = [tx for tx in all_txs if tx.trade_id == fill.trade_id]
    fill._completed_at = max([tx.time for tx in fill._transactions])


"""
bl sh
50 100 = 50

bh sl
100 50 = -50
"""


# seperate into buy/sell
buy_fills = [t for t in all_fills if t.side == "BUY"]
sell_fills = [t for t in all_fills if t.side == "SELL"]

# sort both by _completed_at
sell_fills.sort(_completed_at)
buy_fills.sort(_completed_at, usd_price)


# for each, get the tx at
for sf in sell_fills:
    available_product_buy_fills = [
        bf
        for bf in buy_fills
        if bf.to_product == sf.from_product and bf._registered_size < bf.size
    ]

    # long term distribution
    longterm_apbf = [
        apbf
        for apbf in available_product_buy_fills
        if sf._completed_at - apbf._completed_at >= datetime.year
    ]

    # todo sort by highest price
    lt_apbf_sort = longterm_apbf

    # short term distribution
    shortterm_apbf = [
        apbf for apbf in available_product_buy_fills if apbf not in longterm_apbf
    ]
    # todo sort by highest price
    st_apbf_sort = shortterm_apbf

    # all available in priority sort
    priority_search_apbf: List[Fill] = lt_apbf_sort.extend(st_apbf_sort)

    while sf._registered_size < sf.size:
        for apbf in priority_search_apbf:
            apbf._registered_fills.append(sf)
            sf._registered_fills.append(apbf)

            sf_unregistered_size = sf.size - sf._registered_size
            apbf_unregistered_size = apbf.size - apbf._registered_size

            # choose the smaller size available to register
            registering_size = min(sf_unregistered_size, apbf_unregistered_size)

            apbf._registered_size += registering_size
            sf._registered_size += registering_size
