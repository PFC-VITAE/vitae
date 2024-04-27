from infra.db.dto.candidate_dto import CandidateDTO, CursoDTO

class Candidate:
    def __init__(self, object: CandidateDTO):
        self.full_name = object.nome
        self.cpf = object.cpf
        self.rank = object.posto_grad
        self.qas_qms = object.qas_qms
        self.war_name = object.nome_guerra
        self.promotion_date = object.dt_promocao
        self._id = object._id
        self.dgp_courses = [Course(course) for course in object.cursos]

class Course:
    def __init__(self, object: CursoDTO):
        self.name = object.nome
        self.year_end = object.ano_fim
        self.school = object.estab_ensino
        self.country = object.pais_curso
        self.modality = object.modalidade
