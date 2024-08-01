from types import SimpleNamespace

def dict_to_object(d):
    if isinstance(d, dict):
        obj_dict = {}
        for k, v in d.items():
            if isinstance(v, list):
                obj_dict[k] = [dict_to_object(item) for item in v]
            else:
                obj_dict[k] = dict_to_object(v)
        return SimpleNamespace(**obj_dict)
    else:
        return d