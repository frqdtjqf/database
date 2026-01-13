from dataclasses import dataclass

@dataclass
class WebTable:
    name: str
    columns: list[str]
    rows: list[dict[str, str]]