import pandas as pd

def flatten_json(json_obj):
    """
    Função para planificar um objeto JSON aninhado.
    """
    def _flatten(obj, prefix=''):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    yield from _flatten(v, f"{prefix}{k}_")
                else:
                    yield f"{prefix}{k}", v
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                yield from _flatten(v, f"{prefix}{i}_")
        else:
            yield prefix[:-1], obj

    return dict(_flatten(json_obj))