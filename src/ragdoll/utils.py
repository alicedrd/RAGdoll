import re

def clean_name(name: str) -> str:
    name = re.sub(r"\s+", "_", name.strip())
    name = re.sub(r"[^a-zA-Z0-9_\.\-]", "", name)
    return name