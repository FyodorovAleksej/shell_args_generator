def read_template_from_file(__input_path: str) -> str:
    file = open(__input_path, "r+")
    text = file.read()
    file.close()
    return text
