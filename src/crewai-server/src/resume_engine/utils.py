def read_file(file_path: str) -> str:
    """Read a file and return its contents as a string"""
    with open(file_path, "r") as file:
        return file.read()
