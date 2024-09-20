from core.entities.mission import Mission


class SubmitDocument:

    def __init__(self, mission: Mission):
        self.__document = mission.create_document()

    def execute(self, filepath, pages):
        return self.__document.export_page_content(filepath=filepath, pages=pages)
