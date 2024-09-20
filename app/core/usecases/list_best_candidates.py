from core.interfaces.candidate_repository import ICandidateRepository
from ..interfaces.vector_store import IVectorStore
from ..entities.vectorizer import Vectorizer
from ..entities.candidate_filter import CandidateFilter


class ListBestCandidates:

    def __init__(
        self, candidate_repository: ICandidateRepository, vector_store: IVectorStore
    ):
        self.__candidate_repository = candidate_repository
        self.vector_store = vector_store
        self.vectorizer = Vectorizer()
        self.candidate_filter = CandidateFilter()

    def filter_index(self, vectors, vector_to_text_id, filtered_candidates_cpf):
        filtered_candidates_id = {
            k: v for k, v in vector_to_text_id.items() if v in filtered_candidates_cpf
        }
        filtered_candidates_vectors = [
            vectors[int(k)] for k in filtered_candidates_id.keys()
        ]
        new_vector_to_text_id = {
            str(i): cpf for i, (k, cpf) in enumerate(filtered_candidates_id.items())
        }

        filtered_index = self.vector_store.create_index(filtered_candidates_vectors)
        return filtered_index, new_vector_to_text_id

    def find_similar_candidates(
        self, query_vector, filtered_candidates, index, vector_to_text_id
    ):
        distances, indices = self.vector_store.search_similar(query_vector, index, k=20)
        similar_text_ids = [vector_to_text_id[str(idx)] for idx in indices[0]]
        similar_candidates = []
        for cpf in similar_text_ids:
            for candidate in filtered_candidates:
                if candidate.cpf == cpf:
                    similar_candidates.append(candidate)
                    break
        return similar_candidates

    def get_vectors_index(self):
        vectors_bool = self.vector_store.vectors_exist()
        if vectors_bool:
            index, vector_to_text_id = self.vector_store.get_vectors()
            vectors = index.reconstruct_n(0, index.ntotal)
            return vectors, index, vector_to_text_id
        else:
            return "Não há vetores salvos"

    def execute(self, nce):
        candidates = self.__candidate_repository.get_all_candidates()
        filtered_candidates = self.candidate_filter.apply_filters(
            candidates, mission=nce
        )

        filtered_candidates_cpf = [candidate.cpf for candidate in filtered_candidates]
        vectors, _, vector_to_text_id = self.get_vectors_index()

        filtered_index, new_vector_to_text_id = self.filter_index(
            vectors, vector_to_text_id, filtered_candidates_cpf
        )
        nce_text = f"{nce.application} {nce.knowledge}"
        query_vector = self.vectorizer.vectorize(nce_text)

        similar_candidates = self.find_similar_candidates(
            query_vector, filtered_candidates, filtered_index, new_vector_to_text_id
        )
        return similar_candidates
