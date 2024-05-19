from .mission import Mission
from .nce import NCE

class AcademicCourse(Mission):

    def create_document(self) -> NCE:
        return NCE()
    