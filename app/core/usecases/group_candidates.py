from ..interfaces.object_store import IObjectStore
from ..interfaces.vector_store import IVectorStore
from helpers.dict_to_json import dict_to_json
from ..entities.vectorizer import Vectorizer
from ..entities.cluster_algorithm import ClusterAlgorithm
from ..interfaces.cluster_repository import IClusterRepository
import numpy as np
import os
from helpers.visualize_similarity import find_optimal_eps

class GroupCandidates:
      
    def __init__(self, object_store: IObjectStore, vector_store: IVectorStore, cluster_repository: IClusterRepository):
        self.object_store = object_store
        self.vector_store = vector_store
        self.vectorizer = Vectorizer()
        self.cluster_algorithm = ClusterAlgorithm()
        self.__cluster_repository = cluster_repository
    
    def vectorize_texts(self, objects, vector_to_text_id):
        all_embeddings = np.empty((0, 768))
        curr_vector_id = 0

        for obj in objects:
            data = self.object_store.get_dl_object(object_name=obj)
            data_lattes = self.object_store.get_dl_object(object_name=obj.replace("dgp", "lattes"))
            if data_lattes:
                data += data_lattes
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
    
    def save_clusters(self, labels, centroids, vector_to_text_id):
        clusters = []
        for label in set(labels):
            if label == -1: #Ignore noise
                continue

            cluster = {
                'label': int(label),
                'centroid': centroids[label].tolist(),
                'ids': [],
                'cpfs': []
            }

            for i, l in enumerate(labels):
                if l == label:
                    cluster['ids'].append(i)  
                    cluster['cpfs'].append(vector_to_text_id[str(i)])  

            clusters.append(cluster)

        self.__cluster_repository.insert_clusters(clusters)


    def execute(self):
        vector_to_text_id = {}
        vectors_bool = self.vector_store.vectors_exist()
               
        if vectors_bool: 
            index, vector_to_text_id = self.vector_store.get_vectors()
            vectors = index.reconstruct_n(0, index.ntotal)
        else: 
            objects = self.object_store.list_dl_objects(prefix="trusted/dgp") 
            all_embeddings, vector_to_text_id = self.vectorize_texts(objects, vector_to_text_id)
            index = self.vector_store.save_vectors(all_embeddings, vector_to_text_id) 
            vectors = all_embeddings


        labels = self.cluster_algorithm.dbscan(vectors, ep=10, minPts=1536)
        #labels, centroids = self.cluster_algorithm.kmeans(n=2, X=vectors)

        # self.cluster_algorithm.kmeans_silhoutte(X=vectors)


        #self.save_clusters(labels, centroids, vector_to_text_id)

        #!EXPERIMENTOs CLUSTERING
        # find_optimal_eps(vectors, k=1536)
        # print(self.cluster_algorithm.kmeans(n=6, X=vectors))

        eps_values = [10]
        min_samples_values = [1536]
        # self.cluster_algorithm.test_dbscan_parameters(vectors, eps_values, min_samples_values, use_pca=False)
        print('acabei')