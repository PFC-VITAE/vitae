from core.entities.academic_course import AcademicCourse
from core.usecases.submit_document import SubmitDocument
from core.usecases.consolidate_candidate_data import ConsolidateCandidateData
from core.usecases.list_best_candidates import ListBestCandidates
from core.usecases.regular_strategy import RegularStrategy
from infra.db.repositories.candidate_repository import CandidateRepository
from infra.rpc.vitae_extractor import VitaeExtractor
from infra.faiss.vector_store import VectorStore
from infra.config import vm_ip_addr, vm_port
import xmlrpc.client


def define_nce_dependency():
    return SubmitDocument(AcademicCourse())


def define_candidate_dependency():
    s = xmlrpc.client.ServerProxy(f"http://{vm_ip_addr}:{vm_port}")
    return ConsolidateCandidateData(
        candidate_repository=CandidateRepository(),
        vitae_extractor=VitaeExtractor(server=s),
    )


def define_ranking_dependancy():
    strategy = RegularStrategy(
        candidate_repository=CandidateRepository(), vector_store=VectorStore()
    )
    return ListBestCandidates(strategy)
