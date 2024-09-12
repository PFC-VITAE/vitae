from ..interfaces.object_store import IObjectStore
from ..interfaces.vector_store import IVectorStore
from helpers.dict_to_json import dict_to_json
import numpy as np
from ..entities.vectorizer import Vectorizer
from ..entities.cluster_algorithm import ClusterAlgorithm
import os, json
from helpers.visualize_similarity import *


class GroupCandidates:
      
    def __init__(self, object_store: IObjectStore, vector_store: IVectorStore):
        self.object_store = object_store
        self.vector_store = vector_store
        self.vectorizer = Vectorizer()
        self.cluster_algorithm = ClusterAlgorithm()
    
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
            vectors = index.reconstruct_n(0, index.ntotal)
        else: 
            objects = self.object_store.list_dl_objects(prefix="refined")
            all_embeddings, vector_to_text_id = self.vectorize_texts(objects, vector_to_text_id)
            index = self.vector_store.save_vectors(all_embeddings, vector_to_text_id)
        
        # query_vector = self.vectorizer.vectorize("Desenvolver conhecimentos sobre as propriedades das biocerâmicas para aplicações em odontologia e medicina.")

        # distances, indices = self.vector_store.search_similar(query_vector, index, k=10)

        # similar_text_ids = [vector_to_text_id[str(idx)] for idx in indices[0]]
        # print(similar_text_ids)
        


        # # !EXPERIMENTO SIMILARIDADE

        # query_text = "Desenvolver conhecimentos sobre as propriedades das biocerâmicas para aplicações em odontologia e medicina."
        # query_vector = self.vectorizer.vectorize(query_text)

        # distances, indices = self.vector_store.search_similar(query_vector, index, k=15)

        # similar_text_ids = [vector_to_text_id[str(idx)] for idx in indices[0]]
        # print(similar_text_ids)
        # print(distances)

        # similar_vectors = vectors[indices[0]]
        # # visualize_similarity_results(query_text, similar_text_ids, distances[0])
        # # visualize_similarity_results_with_query(query_vector, similar_vectors, similar_text_ids, perplexity=min(5, len(similar_vectors)-1))
     

        #!EXPERIMENTO CLUSTERING
        eps_values = [5, 7]
        min_samples_values = [769, 1536]

        find_optimal_eps(vectors, k=1536)

        print(self.cluster_algorithm.dbscan(vectors, ep=9.3, minPts=1536))

        # self.cluster_algorithm.test_dbscan_parameters(vectors, eps_values, min_samples_values, use_pca=True)
        # self.cluster_algorithm.test_dbscan_parameters(vectors, eps_values, min_samples_values, use_pca=False)
        
