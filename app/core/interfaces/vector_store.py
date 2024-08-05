from abc import ABC, abstractmethod

class IVectorStore(ABC):

    @abstractmethod
    def save_vectors(self, index, vector_to_text_id):
        pass

    @abstractmethod
    def get_vectors(self):
        pass
    
    @abstractmethod
    def vectors_exist(self):
        pass
    
    @abstractmethod
    def search_similar(self, query_vector, index, k):
        pass
