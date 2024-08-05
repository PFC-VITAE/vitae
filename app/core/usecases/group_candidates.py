from ..interfaces.object_store import IObjectStore
from ..interfaces.vector_store import IVectorStore
from helpers.dict_to_json import dict_to_json
import numpy as np
from ..entities.vectorizer import Vectorizer
import os, json


class GroupCandidates:
      
    def __init__(self, object_store: IObjectStore, vector_store: IVectorStore):
        self.object_store = object_store
        self.vector_store = vector_store
        self.vectorizer = Vectorizer()
    
    def vectorize_texts(self, objects, vector_to_text_id):
        all_embeddings = np.empty((0, 768))
        curr_vector_id = 0

        for obj in objects:
            data = self.object_store.get_dl_object(object_name=obj)
            text_id = os.path.splitext(os.path.basename(obj))[0]

            segments_embeddings, vector_to_text_id, curr_vector_id = self.vectorizer.vectorize_text(
                text=data,
                text_id=text_id,
                curr_vector_id=curr_vector_id,
                vector_to_text_id=vector_to_text_id
            )
            all_embeddings = np.vstack((all_embeddings, segments_embeddings))
            print(f"Vectors for {obj} created.")
        

        return all_embeddings, dict_to_json(vector_to_text_id)
            

    def execute(self):
        vector_to_text_id = {}
        vectors_bool = self.vector_store.vectors_exist()
               
        if vectors_bool: 
            index, vector_to_text_id = self.vector_store.get_vectors()
        else: 
            objects = self.object_store.list_dl_objects(prefix="refined")
            all_embeddings, vector_to_text_id = self.vectorize_texts(objects, vector_to_text_id)
            index = self.vector_store.save_vectors(all_embeddings, vector_to_text_id)
        
        query_vector = self.vectorizer.vectorize("Desenvolver conhecimentos sobre as propriedades das biocerâmicas para aplicações em odontologia e medicina.")

        distances, indices = self.vector_store.search_similar(query_vector, index, k=10)

        similar_text_ids = [vector_to_text_id[str(idx)] for idx in indices[0]]
        print(similar_text_ids)
        

        
        


