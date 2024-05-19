from core.usecases.consolidate_candidate_data import ConsolidateCandidateData
from infra.db.candidate_repository import CandidateRepository
from infra.services.vitae_extractor import VitaeExtractor
from infra.config import vm_ip_addr, vm_port
import xmlrpc.client


s = xmlrpc.client.ServerProxy(f"http://{vm_ip_addr}:{vm_port}")

if __name__ == "__main__":

    repository = CandidateRepository()
    vitae_extrator = VitaeExtractor(server=s)

    usecase_consolidate_candidate_data = ConsolidateCandidateData(candidate_repository=repository, vitae_extractor=vitae_extrator)
    
    usecase_consolidate_candidate_data.execute()
