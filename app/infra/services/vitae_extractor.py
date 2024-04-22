from core.interfaces.vitae_extractor import IVitaeExtractor
from infra.config import extrator_lattes_url
from zeep import Client
import zipfile
import os

class VitaeExtractor(IVitaeExtractor):
    
    def __init__(self, wsdl_url=extrator_lattes_url):
        self.__client = Client(wsdl_url)
        self.wsdl_url = wsdl_url

    def getID(self, cpf, full_name, birth_date):
        return self.__client.service.getIdentificadorCNPq(
            cpf=cpf, 
            nomeCompleto=full_name, 
            dataNascimento=birth_date
        )
                  

    def getVitae(self, id):
        vitae_zip = self.__client.service.getCurriculoCompactado(id=id)

        if vitae_zip:
            with open('./app/data/temp.zip', 'wb') as f:
                f.write(vitae_zip)

            xml_vitae = f"{id}.xml"
            with zipfile.ZipFile('./app/data/temp.zip', 'r') as f:
                f.extract(xml_vitae, "./app/data/cv")
            
            with open(os.path.join("./app/data/cv", xml_vitae), 'r', encoding='iso-8859-1') as f:
                vitae_content = f.read()
        
        if os.path.exists('./app/data/temp.zip'):
            os.remove('./app/data/temp.zip')
        if os.path.exists(os.path.join("./app/data/cv", xml_vitae)):
            os.remove(os.path.join("./app/data/cv", xml_vitae))

        return vitae_content