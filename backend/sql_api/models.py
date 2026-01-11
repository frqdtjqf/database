from dataclasses import dataclass

# ein Attribut einer Tabelle
@dataclass
class Attribute:
    name: str
    type: str
    primary_key: bool = False

# eine Tabelle in der Datenbank
@dataclass
class Table:
    name: str
    attributes: list[Attribute]

# ein Element eines Datensatzes, ordnet einem Wert ein Attribut zu
# validiert den Wert entsprechend dem Attributtyp bei der Initialisierung
@dataclass
class Element:
    attribute: Attribute
    value: any

    def __post_init__(self):
        self.validate()

    def validate(self) -> bool:
        """Validate that the value matches the attribute type."""
        if self.value is None:
            return True  # Allow NULLs
        
        sql_type = self.attribute.type.upper()
        if sql_type == "INTEGER":
            if not isinstance(self.value, int):
                raise TypeError(f"Attribute {self.attribute.name} expects int, got {type(self.value).__name__}")
        elif sql_type == "REAL":
            if not isinstance(self.value, (float, int)):
                raise TypeError(f"Attribute {self.attribute.name} expects float, got {type(self.value).__name__}")
        elif sql_type == "TEXT":
            if not isinstance(self.value, str):
                raise TypeError(f"Attribute {self.attribute.name} expects str, got {type(self.value).__name__}")
        elif sql_type == "BLOB":
            if not isinstance(self.value, bytes):
                raise TypeError(f"Attribute {self.attribute.name} expects bytes, got {type(self.value).__name__}")
        else:
            raise TypeError(f"Unknown SQL type {self.attribute.type} for attribute {self.attribute.name}")
        return True

# einen Datensatz in der Tabelle, Sammlung von Werten zu den Attributen der Tabelle
@dataclass
class Record:
    elements: list[Element]

    def get_primary_key_element(self) -> Element:
        for e in self.elements:
            if e.attribute.primary_key:
                return e
        raise ValueError("No primary key element found in record")