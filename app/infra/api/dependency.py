from core.entities.academic_course import AcademicCourse
from core.usecases.submit_document import SubmitDocument
from core.usecases.consolidate_candidate_data import ConsolidateCandidateData
from infra.db.candidate_repository import CandidateRepository
from infra.services.vitae_extractor import VitaeExtractor
from infra.config import vm_ip_addr, vm_port
import xmlrpc.client

def define_nce_dependency():
    return SubmitDocument(AcademicCourse())

def define_candidate_dependency():
    s = xmlrpc.client.ServerProxy(f"http://{vm_ip_addr}:{vm_port}")
    
    repository = CandidateRepository()
    vitae_extrator = VitaeExtractor(server=s)

    return ConsolidateCandidateData(candidate_repository=repository, vitae_extractor=vitae_extrator)