from abc import ABC, abstractmethod

class Document(ABC):

    @abstractmethod
    def export_page_content(self, pages):
        pass