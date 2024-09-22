import zipfile
import os
from core.interfaces.vitae_extractor import IVitaeExtractor


class VitaeExtractor(IVitaeExtractor):

    def __init__(self, server):
        self.__server = server

    def get_ID(self, cpf, full_name, birth_date):
        try:
            return self.__server.get_ID(cpf, full_name, birth_date)

        except Exception as e:
            raise ValueError("Erro ao buscar ID no Extractor") from e

    def get_vitae(self, id):
        try:
            vitae_zip = self.__server.get_vitae(id).data

            if vitae_zip:
                with open("./app/infra/storage/data/temp.zip", "wb") as f:
                    f.write(vitae_zip)

                xml_vitae = f"{id}.xml"
                with zipfile.ZipFile("./app/infra/storage/data/temp.zip", "r") as f:
                    f.extract(xml_vitae, "./app/infra/storage/data/cv")

                with open(
                    os.path.join("./app/infra/storage/data/cv", xml_vitae),
                    "r",
                    encoding="iso-8859-1",
                ) as f:
                    vitae_content = f.read()

            if os.path.exists("./app/infra/storage/data/temp.zip"):
                os.remove("./app/infra/storage/data/temp.zip")
            if os.path.exists(os.path.join("./app/infra/storage/data/cv", xml_vitae)):
                os.remove(os.path.join("./app/infra/storage/data/cv", xml_vitae))

            return vitae_content

        except Exception as e:
            raise ValueError("Erro ao buscar CV no Extractor") from e
