from abc import ABC, abstractmethod
from .document import Document

class Mission(ABC):

    @abstractmethod
    def create_document(self) -> Document:
        pass
