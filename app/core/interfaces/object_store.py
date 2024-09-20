from abc import ABC, abstractmethod


class IObjectStore(ABC):

    @abstractmethod
    def insert_dl_resume(self, cpf, resume, file_extension):
        pass

    @abstractmethod
    def list_dl_objects(self, prefix):
        pass

    @abstractmethod
    def get_dl_object(self, object_name):
        pass
