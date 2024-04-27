from core.entities.academic_course import AcademicCourse
from core.usecases.submit_document import SubmitDocument

def define_nce_dependency():
    return SubmitDocument(AcademicCourse())
