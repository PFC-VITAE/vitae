from infra.db.dto.candidate_dto import CandidateDTO, CursoDTO

class Candidate:
    def __init__(self, object):
        self._id = object._id
        self.full_name = object.full_name
        self.cpf = object.cpf
        self.rank = object.rank
        self.birth_date = object.birth_date
        self.qas_qms = object.qas_qms
        self.war_name = object.war_name
        self.promotion_date = object.promotion_date
        self.dgp_courses = [Course(course) for course in object.dgp_courses]
        self.updated_last = getattr(object, 'updated_last', None)
        self.resume = getattr(object, 'resume', None)


    def to_dict(self):
        candidate_dict = self.__dict__.copy()
        candidate_dict['dgp_courses'] = [course.__dict__ for course in self.dgp_courses]
        return candidate_dict
        

class Course:
    def __init__(self, object):
        self.name = object.name
        self.year_end = object.year_end
        self.school = object.school
        self.country = object.country
        self.modality = object.modality
