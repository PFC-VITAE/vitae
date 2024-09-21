from ..interfaces.ranking_strategy import RankingStrategy


class ListBestCandidates:

    def __init__(self, strategy: RankingStrategy):
        self.__strategy = strategy

    def execute(self, nce):
        return self.__strategy.execute(nce)
