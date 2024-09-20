from abc import ABC, abstractmethod


class IClusterRepository(ABC):

    @abstractmethod
    def insert_clusters(self, clusters_list):
        pass

    @abstractmethod
    def get_all_clusters(self):
        pass
