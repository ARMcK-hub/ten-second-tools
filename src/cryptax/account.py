from cryptax.coinbase_pro import CoinbaseProTransactionFactory
from cryptax.core import ReportGenerator

"""
This is intended to be the proper implementation of cryptax, but is a work in progress.
"""

# txs_file = "/workspaces/ten-second-tools/src/cryptax/data/account_CoinbasePro_2021.csv"
txs_file = (
    "/workspaces/ten-second-tools/src/cryptax/data/test/test_account_transactions.csv"
)

STRATEGY = "lowest"

cbff = CoinbaseProTransactionFactory()
txs = cbff.get_transactions(txs_file)

report_generator = ReportGenerator()

report_generator.add_transactions(txs)

# report = report_generator.report(STRATEGY)

# report.to_terminal()

strat = report_generator._get_strategy(STRATEGY)

strat.recognize_taxable_transactions(
    report_generator._taxable_distributions, report_generator._acquisitions
)
