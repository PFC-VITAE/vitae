from ..interfaces.ranking_strategy import RankingStrategy
from ..interfaces.candidate_repository import ICandidateRepository
from ..interfaces.vector_store import IVectorStore
from ..entities.vectorizer import Vectorizer
from ..entities.candidate_filter import CandidateFilter
from ..interfaces.cluster_repository import IClusterRepository

nce = {
    "código": "42M2025 (Muito Alta)",
    "posto": "1º Ten, Cap",
    "perfil": "QEM Compt",
    "conhecimento_específico": "Algoritmos de Aprendizado de Máquina Aplicados à Detecção Automática de Comportamento Suspeito em Redes Sociais.",
    "aplicação": "Defesa Cibernética, Segurança da Informação, Capacitação de Recursos Humanos na forma de pessoal para os cursos de graduação no IME, principalmente na área de Engenharia da Computação.",
    "programa": "Engenharia de Defesa (PGED)",
}


class ClusterStrategy(RankingStrategy):

    def __init__(
        self,
        candidate_repository: ICandidateRepository,
        vector_store: IVectorStore,
        cluster_repository: IClusterRepository,
    ):
        self.__candidate_repository = candidate_repository
        self.vector_store = vector_store
        self.vectorizer = Vectorizer()
        self.candidate_filter = CandidateFilter()
        self.__cluster_repository = cluster_repository

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
                    similar_candidates.append(candidate.full_name)
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

    def get_nearest_cluster(self, query_vector, clusters):
        distances = []
        for cluster in clusters:
            distance = self.vector_store.calculate_distance(
                query_vector, cluster.centroid
            )
            distances.append(distance)
        nearest_cluster_index = distances.index(min(distances))
        nearest_cluster = clusters[nearest_cluster_index]
        return nearest_cluster

    def get_cluster_vectors(self, vectors, cluster):
        cluster_candidates_id = cluster.ids
        cluster_candidates_cpfs = cluster.cpfs
        cluster_candidates_vectors = [vectors[int(k)] for k in cluster_candidates_id]
        new_vector_to_text_id = {
            str(i): cpf
            for i, (k, cpf) in enumerate(
                zip(cluster_candidates_id, cluster_candidates_cpfs)
            )
        }

        return new_vector_to_text_id, cluster_candidates_vectors

    def execute(self):
        candidates = self.__candidate_repository.get_all_candidates()

        vectors, index, vector_to_text_id = self.get_vectors_index()

        self.clusters = self.__cluster_repository.get_all_clusters()

        nce_text = f"{nce['aplicação']} {nce['conhecimento_específico']}"

        query_vector = self.vectorizer.vectorize(nce_text)

        nearest_cluster = self.get_nearest_cluster(query_vector, self.clusters)

        nearest_cluster_mapping, nearest_cluster_vectors = self.get_cluster_vectors(
            vectors, nearest_cluster
        )

        nearest_cluster_candidates = [
            candidate
            for candidate in candidates
            if candidate.cpf in nearest_cluster.cpfs
        ]

        filtered_candidates = self.candidate_filter.apply_filters(
            nearest_cluster_candidates, mission=nce
        )

        filtered_candidates_cpf = [candidate.cpf for candidate in filtered_candidates]

        filtered_index, new_vector_to_text_id = self.filter_index(
            nearest_cluster_vectors, nearest_cluster_mapping, filtered_candidates_cpf
        )

        similar_candidates = self.find_similar_candidates(
            query_vector, filtered_candidates, filtered_index, new_vector_to_text_id
        )
        print(similar_candidates)
        return similar_candidates
