from typing import Dict

from cryptax.core.cost_basis import CostBasisStrategy


class CostBasisStrategyFactory:
    def get_strategy(
        self, strategy_name: str, strategy_config: Dict[str, str] = {}
    ) -> CostBasisStrategy:
        # TODO: import all strategies & return strategy with name
        strategy = self.get_all_strategies().get(strategy_name)

        return strategy(strategy_config)

    def get_all_strategies(self) -> Dict[str, CostBasisStrategy]:
        return {strat.name: strat for strat in CostBasisStrategy.__subclasses__()}
