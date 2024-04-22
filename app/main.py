from usecases.submit_nce import SubmitNCE

if __name__ == "__main__":
    sb = SubmitNCE()
    df = sb.extract_content()
    print(df)