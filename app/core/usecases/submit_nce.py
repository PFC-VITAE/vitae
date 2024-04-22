import multiprocessing
from core.entities.nce import NCE

class SubmitNCE:

    def extract_content(self, filepath):
        document = NCE(filepath)
        with multiprocessing.Pool(processes=4) as pool:
            page_list = document.file_pages()
            return pool.map(document.export_page_content, list(range(4, 6)))
