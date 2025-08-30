from src.api.core.cost.calculation.interface_cost import InterfaceCost


class BaseCost(InterfaceCost):
    def _calculate_cost(self, tokens: int, unit_of_measure: int, value: float) -> float:
        return (tokens / unit_of_measure) * value

    def _calculate_total_cost(
        self, completion_cost: float, prompt_cost: float
    ) -> float:
        return round(completion_cost + prompt_cost, 6)
