import json, faiss, os
from core.interfaces.vector_store import IVectorStore
import numpy as np

class VectorStore(IVectorStore):

    def __init__(self, d=768):
        self.index = faiss.IndexFlatL2(d)
        self.base_path = "app/infra/storage/data/vectors/"
        self.index_file_path = self.base_path + "faiss_index.idx"
        self.ids_file_path = self.base_path + "vector_to_text_id.json"
        os.makedirs(self.base_path, exist_ok=True)     

    def save_vectors(self, embeddings, vector_to_text_id):
        self.index.add(embeddings)
        faiss.write_index(self.index, self.index_file_path)
        with open(self.ids_file_path, 'w') as f:
            json.dump(vector_to_text_id, f)
        return self.index

    def get_vectors(self):
        index = faiss.read_index(self.index_file_path)
        with open(self.ids_file_path, 'r') as f:
            vector_to_text_id = json.load(f)
        return index, vector_to_text_id

    def vectors_exist(self):
        return os.path.exists(self.index_file_path) and os.path.exists(self.ids_file_path)
     
    def search_similar(self, query_vector, index, k):
        D, I = index.search(query_vector, k)
        return D, I

    def create_index(self, vectors):
        index = faiss.IndexFlatL2(768)
        index.add(np.array(vectors))
        return index
    
    def calculate_distance(self, query_vector, centroid):
        return np.linalg.norm(query_vector - centroid)