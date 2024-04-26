from core.entities.nce import NCE

class SubmitNCE:

    def execute(self, filepath, pages):
        document = NCE(filepath)
        return document.export_page_content(pages)
