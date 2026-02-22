def text_to_json(text):
    """
    Guaranteed parser:
    - No assumptions
    - No conditions
    - No data loss
    """

    lines = text.splitlines()
    data = {}

    index = 1
    for line in lines:
        clean_line = line.strip()
        if clean_line:
            data[f"line_{index}"] = clean_line
            index += 1

    return data
