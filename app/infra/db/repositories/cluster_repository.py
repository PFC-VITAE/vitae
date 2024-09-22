from core.interfaces.cluster_repository import IClusterRepository
from infra.db.connection import db_connection
from helpers.dict_to_object import *


class ClusterRepository(IClusterRepository):

    def __init__(self, db_client=db_connection):
        self.__db_client = db_client

    def insert_clusters(self, clusters_list):
        try:
            db = self.__db_client["vitae"]
            collection = db["clusters"]

            for cluster in clusters_list:
                cluster_id = cluster.get("_id")

                if cluster_id:
                    collection.replace_one({"_id": cluster_id}, cluster, upsert=True)
                else:
                    collection.insert_one(cluster)

            return "Dados inseridos ou atualizados com sucesso"

        except Exception as e:
            raise ValueError("Erro ao inserir dados no banco") from e

    def get_all_clusters(self):
        try:
            db = self.__db_client["vitae"]
            collection = db["clusters"]
            documents = list(collection.find())

            clusters_data = [(dict_to_object(doc)) for doc in documents]

            return clusters_data

        except Exception as e:
            raise ValueError("Erro ao buscar dados no banco") from e
