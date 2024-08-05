def dict_to_json(d):
    if not isinstance(d, dict):
        raise ValueError("O argumento deve ser um dicionário.")
    
    return {str(k): v for k, v in d.items()}

