from core.interfaces.candidate_repository import ICandidateRepository
from ..dto.candidate_dto import CandidateDTO
from ..connection import dgp_connection, db_connection
from helpers.dict_to_object import *


class CandidateRepository(ICandidateRepository):

    def __init__(self, dgp_client=dgp_connection, db_client=db_connection):
        self.__dgp_client = dgp_client
        self.__db_client = db_client

    def get_all_personal_info(self):
        try:
            db = self.__dgp_client["DGP_mock"]
            collection = db["personal_data"]
            documents = list(collection.find())

            candidates_data = [CandidateDTO.from_dict(doc) for doc in documents]

            return candidates_data

        except Exception as e:
            raise ValueError("Erro ao buscar dados no banco DGP") from e

    def insert_candidates(self, candidates_list):
        try:
            db = self.__db_client["vitae"]
            collection = db["candidates"]

            candidates_dict_list = [candidate.__dict__ for candidate in candidates_list]

            for candidate in candidates_dict_list:
                candidate_id = candidate.get("_id")

                if candidate_id:
                    collection.replace_one(
                        {"_id": candidate_id}, candidate, upsert=True
                    )
                else:
                    collection.insert_one(candidate)

            return "Dados inseridos ou atualizados com sucesso"

        except Exception as e:
            raise ValueError("Erro ao inserir dados no banco") from e

    def get_all_candidates(self):
        try:
            db = self.__db_client["vitae"]
            collection = db["candidates"]
            documents = list(collection.find())

            candidates_data = [(dict_to_object(doc)) for doc in documents]

            return candidates_data

        except Exception as e:
            raise ValueError("Erro ao buscar dados no banco") from e
