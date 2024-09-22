def json_to_string(data):
    result = ""

    if isinstance(data, dict):
        for key, value in data.items():
            result += f"{key}: "
            if isinstance(value, (dict, list)):
                result += json_to_string(value)
            else:
                result += f"{value} "
    elif isinstance(data, list):
        for item in data:
            result += json_to_string(item)
    else:
        result += f"{data} "

    return result.strip()
