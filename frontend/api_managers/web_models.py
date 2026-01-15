from dataclasses import dataclass

@dataclass
class WebTable:
    name: str
    entity: str
    columns: list[str]
    rows: list[dict[str, str]]