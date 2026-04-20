import re


def url_to_snake_case(url: str, replacer: str = "_") -> str:
    return re.sub(r"[^a-zA-Z0-9_]+", replacer, url).strip(replacer)
