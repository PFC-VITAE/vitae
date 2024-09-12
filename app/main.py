import uvicorn
from infra.api.server import app

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)

from core.usecases.group_candidates import GroupCandidates
from infra.dl.object_storage import ObjectStore
from infra.db.vector_store import VectorStore

object_store = ObjectStore()
v_store = VectorStore()

usecase = GroupCandidates(object_store=object_store, vector_store=v_store)
usecase.execute()

# from core.usecases.list_best_candidates import ListBestCandidates
# from infra.db.candidate_repository import CandidateRepository

# candidate_repository = CandidateRepository()
# usecase = ListBestCandidates(candidate_repository=candidate_repository, vector_store=v_store)
# usecase.execute()