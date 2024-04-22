from abc import ABC, abstractmethod

class Document(ABC):

    @abstractmethod
    def file_pages(self):
        pass

    @abstractmethod
    def export_page_content(self, page):
        pass