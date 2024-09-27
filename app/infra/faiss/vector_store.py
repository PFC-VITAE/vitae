import json, faiss, os
import numpy as np
from core.interfaces.vector_store import IVectorStore


class VectorStore(IVectorStore):

    def __init__(self, d=768):
        self.__base_path = "app/infra/faiss/vectors/"
        self.__index_file_path = self.__base_path + "faiss_index.idx"
        self.__ids_file_path = self.__base_path + "vector_to_text_id.json"
        os.makedirs(self.__base_path, exist_ok=True)

    def save_vectors(self, embeddings, vector_to_text_id):
        index = faiss.IndexFlatIP(768)
        index.add(embeddings)
        faiss.write_index(index, self.__index_file_path)
        with open(self.__ids_file_path, 'w') as f:
            json.dump(vector_to_text_id, f)
        return index

    def get_vectors(self):
        index = faiss.read_index(self.__index_file_path)
        with open(self.__ids_file_path, 'r') as f:
            vector_to_text_id = json.load(f)
        return index, vector_to_text_id

    def vectors_exist(self):
        return os.path.exists(self.__index_file_path) and os.path.exists(
            self.__ids_file_path
        )
     
    def search_similar(self, query_vector, index, k):
        if not isinstance(query_vector, np.ndarray):
            query_vector = np.array(query_vector, dtype=np.float32)
        elif query_vector.dtype != np.float32:
            query_vector = query_vector.astype(np.float32)

        faiss.normalize_L2(query_vector)
        D, I = index.search(query_vector, k)
        return D, I

    def create_index(self, vectors):
        if not isinstance(vectors, np.ndarray):
            vectors = np.array(vectors, dtype=np.float32)
        elif vectors.dtype != np.float32:
            vectors = vectors.astype(np.float32)

        index = faiss.IndexFlatIP(768)
        faiss.normalize_L2(vectors)
        index.add(np.array(vectors))
        return index
    
    def calculate_distance(self, query_vector, centroid):
        return np.linalg.norm(query_vector - centroid)