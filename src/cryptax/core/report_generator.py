import csv
import os
from typing import Any, Dict, List, Optional, Tuple, Type
from uuid import uuid4

from cryptax.core.cost_basis import CostBasisStrategy

from .transactions.transaction import Acquisition, Distribution, Transaction


class Report:
    def __init__(self) -> None:
        self.id = uuid4()

    def to_csv(self, output_path: str) -> None:
        raise NotImplementedError

    def _write_to_csv(self, filepath: str, rows: List[Dict[str, Any]]) -> None:
        assert os.path.isdir(filepath)

        header = rows[0].keys()
        unpacked_rows = [d.values() for d in rows]

        data = [header, *unpacked_rows]

        with open(filepath, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)


class TaxReport(Report):
    def __init__(
        self, strategy: CostBasisStrategy, fulfilled_transactions: List[Transaction]
    ) -> None:
        self.strategy = strategy
        self.fulfilled_transactions = fulfilled_transactions
        self.gain: Optional[float] = None
        super().__init__()

    def to_csv(self, output_path: str) -> None:
        # should write all reports to csv (unrecognized purchase fills, turbo_tax gain/loss report, gain/loss summary, full gain/loss report)
        """Gain / Loss Report:
        Currency Name
        Purchase Date
        Cost Basis (purchase $)
        Date Sold
        Proceeds (sell $)"""

        # self.__write_to_csv()
        raise NotImplementedError

    def to_terminal(self) -> None:
        for tx in self.fulfilled_transactions:
            print(
                f"{tx.id}  -  Amount Unrecorgnized: {tx.amount - tx.amount_recognized} Fulfillment Txs: {tx.fulfillment_transactions}"
            )


class ReportGenerator:
    def __init__(self) -> None:
        self._all_transactions: Tuple[Transaction] = tuple()
        self._acquisitions: Tuple[Acquisition] = tuple()
        self._taxable_distributions: Tuple[Distribution] = tuple()
        self._reports: List[Report] = []
        self._strategies: Dict[
            Type[CostBasisStrategy], CostBasisStrategy
        ] = self.__get_all_strategies()

    def _get_strategy(self, strategy: str) -> CostBasisStrategy:
        return self._strategies.get(strategy)

    def __get_all_strategies(
        self, strategy_config: Dict[str, str] = {}
    ) -> Dict[Type[CostBasisStrategy], CostBasisStrategy]:
        return {
            strat.name: strat(strategy_config)
            for strat in CostBasisStrategy.__subclasses__()
        }

    def add_transactions(self, transactions: List[Transaction]) -> None:
        self._all_transactions += tuple(transactions)
        self._acquisitions += tuple(
            [tx for tx in transactions if isinstance(tx, Acquisition)]
        )
        self._taxable_distributions += tuple(
            [
                tx
                for tx in transactions
                if isinstance(tx, Distribution) and tx.is_taxable
            ]
        )

    def generate_report(self, cost_basis_strategy: CostBasisStrategy) -> str:
        # generates a single report from a strategy and saves it for later usage
        evaluation = cost_basis_strategy.evaluate()

        report = TaxReport(evaluation)
        self._reports.append(report)
        return report.id

    def generate_reports(
        self, cost_basis_strategies: List[CostBasisStrategy]
    ) -> List[str]:
        # generates multiple reports from a list of strategies and saves them for later usage

        reports = [Report()]
        self._reports.extend(reports)
        return [r.id for r in reports]

    def get_report(self, report_id: str) -> Report:
        # returns a report of a given id from the managed report list
        return [r for r in self._reports if r.id == report_id][0]

    def report(self, cost_basis_strategy: CostBasisStrategy) -> Report:
        # returns a report directly instead of an id for later usage
        report_id = self.generate_report(cost_basis_strategy)
        return self.get_report(report_id)


class TaxReportGenerator(ReportGenerator):
    def __init__(self) -> None:
        super().__init__()
        self._reports: List[TaxReport] = []

    def get_lowest_taxable_report(self) -> Report:
        lowest_taxes = min([r.gain for r in self._reports])
        lowest_tax_report_id = [r.id for r in self._reports if r.gain == lowest_taxes][
            0
        ]
        return self.get_report(lowest_tax_report_id)
