from abc import ABC, abstractmethod

class IObjectStore(ABC):

    @abstractmethod
    def insert_dl_resume(self, cpf, resume, file_extension):
        pass

    @abstractmethod
    def list_dl_objects(self):
        pass
