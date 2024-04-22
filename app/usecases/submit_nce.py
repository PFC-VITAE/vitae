import multiprocessing
from domain.entities.nce import NCE

class SubmitNCE:

    def extract_content(self):
        document = NCE("./app/data/sepbe51-21_port_113-dct.pdf")
        with multiprocessing.Pool(processes=4) as pool:
            page_list = document.file_pages()
            return pool.map(document.export_page_content, list(range(4, 6)))
        # return document.export_page_content("4-105")
