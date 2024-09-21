from abc import ABC, abstractmethod


class RankingStrategy(ABC):

    @abstractmethod
    def filter_index():
        pass

    @abstractmethod
    def filter_index(self, vectors, vector_to_text_id, filtered_candidates_cpf):
        pass

    def get_vectors_index(self, query_vector, filtered_candidates, index, vector_to_text_id):
        pass

    @abstractmethod
    def execute(self, nce):
        pass