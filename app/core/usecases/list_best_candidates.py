from core.interfaces.candidate_repository import ICandidateRepository
from ..interfaces.vector_store import IVectorStore
from ..entities.vectorizer import Vectorizer
from ..entities.candidate_filter import CandidateFilter
import re

nce = {
    "código": "42M2025 (Muito Alta)",
    "posto": "1º Ten, Cap", 
    "perfil": "QEM Compt",
    "conhecimento_específico": "Algoritmos de Aprendizado de Máquina e Modelos de Linguagem Aplicados à Interação entre Humanos e Máquinas.",
    "aplicação": "Defesa Cibernética, Segurança da Informação, Capacitação de Recursos Humanos na forma de pessoal para os cursos de graduação no IME, principalmente na área de Engenharia da Computação.",
    "programa": "Engenharia de Defesa (PGED)",
}

def determine_degree_type(code):
    if 'D' in code:
        return 'Doutorado'
    elif 'M' in code:
        return 'Mestrado'
    return 'Indefinido'


class ListBestCandidates:

    def __init__(self, candidate_repository: ICandidateRepository, vector_store: IVectorStore):
        self.__candidate_repository = candidate_repository
        self.vector_store = vector_store
        self.vectorizer = Vectorizer()
        self.candidate_filter = CandidateFilter()
    
       
    def filter_index(self, index, vectors, vector_to_text_id, filtered_candidates_cpf):
        filtered_candidates_id = {k: v for k, v in vector_to_text_id.items() if v in filtered_candidates_cpf}
        filtered_candidates_vectors = [vectors[int(k)] for k in filtered_candidates_id.keys()]
        new_vector_to_text_id = {str(i): cpf for i, (k, cpf) in enumerate(filtered_candidates_id.items())}

        filtered_index = self.vector_store.create_index(filtered_candidates_vectors)
        return filtered_index, new_vector_to_text_id

    def find_similar_candidates(self, query_vector, filtered_candidates, index, vector_to_text_id):
        distances, indices = self.vector_store.search_similar(query_vector, index, k=10)
        similar_text_ids = [vector_to_text_id[str(idx)] for idx in indices[0]]
        return [candidate.full_name for candidate in filtered_candidates if candidate.cpf in similar_text_ids]

    def get_vectors_index(self):
        vectors_bool = self.vector_store.vectors_exist()
        if vectors_bool:
            index, vector_to_text_id = self.vector_store.get_vectors()
            vectors = index.reconstruct_n(0, index.ntotal)
            return vectors, index, vector_to_text_id
        else:
            return "Não há vetores salvos"
    
    def execute(self):
        candidates = self.__candidate_repository.get_all_candidates()

        #TODO: implementar filtro de mestrado/doutorado 
        nce['degree_type'] = determine_degree_type(nce["código"])

        filtered_candidates = self.candidate_filter.apply_filters(candidates, mission=nce)

        filtered_candidates_cpf = [candidate.cpf for candidate in filtered_candidates]

        vectors, index, vector_to_text_id = self.get_vectors_index()

        filtered_index, new_vector_to_text_id = self.filter_index(index, vectors, vector_to_text_id, filtered_candidates_cpf)

        query_vector = self.vectorizer.vectorize({
            "conhecimento_específico": nce["conhecimento_específico"],
            "aplicação": nce["aplicação"]
        })
   
        similar_candidates = self.find_similar_candidates(query_vector, filtered_candidates, filtered_index, new_vector_to_text_id)
        return similar_candidates
    
    
    

