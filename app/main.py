from core.usecases.submit_nce import SubmitNCE

if __name__ == "__main__":
    submition_usecase = SubmitNCE()
    df = submition_usecase.extract_content("./app/data/sepbe51-21_port_113-dct.pdf", "1-10")