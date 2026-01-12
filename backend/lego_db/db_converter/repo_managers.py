from backend.lego_db.lego_models import LegoPart, TemplateMinifigure, ActualMinifigure, Weapon
from backend.sql_api import Table, Record, Element
from backend.lego_db.db_converter.convert_rules import LEGO_PART_TABLE, TEMPLATE_MINIFIGURE_TABLE, ACTUAL_MINIFIGURE_TABLE, WEAPON_TABLE
from backend.sql_api import DataBaseWrapper

class BaseRepoManager:
    table: Table

    def __init__(self, db: DataBaseWrapper):
        self.db = db

    # --- Write Models ---
    def add_model(self, obj: LegoPart|TemplateMinifigure|ActualMinifigure|Weapon):
        record = self._to_record(obj)
        self.db.insert_record(self.table, record)

    def delete_model(self, obj: LegoPart|TemplateMinifigure|ActualMinifigure|Weapon):
        record = self._to_record(obj)
        self.db.delete_record(self.table, record)

    # --- Read Models ---
    def get_models(self) -> list[LegoPart|TemplateMinifigure|ActualMinifigure|Weapon]:
        records = self.db.get_records(self.table)
        return [self._from_record(record) for record in records]

    # --- Table Management ---
    def delete_table(self):
        self.db.delete_table(self.table)

    def create_table(self):
        self.db.create_table(self.table)

    # --- Helpers ---
    def get_model_by_primary_key(self, pk_value: str) -> LegoPart|TemplateMinifigure|ActualMinifigure|Weapon | None:
        models = self.get_models()
        for model in models:
            record = self._to_record(model)
            pk_element = record.get_primary_key_element()
            if pk_element.value == pk_value:
                return model
            
    # --- Helpers to be implemented in subclasses ---
    def _to_record(self, obj: LegoPart|TemplateMinifigure|ActualMinifigure|Weapon) -> Record:
        raise NotImplementedError
    
    def _from_record(self, record: Record) -> LegoPart|TemplateMinifigure|ActualMinifigure|Weapon:
        raise NotImplementedError

class LegoPartRepoManager(BaseRepoManager):
    table = LEGO_PART_TABLE

    def _to_record(self, part: LegoPart) -> Record:
        return Record(elements=[
            Element(attr, getattr(part, attr.name)) for attr in self.table.attributes
        ])
    
    def _from_record(self, record: Record) -> LegoPart:
        data = {e.attribute.name: e.value for e in record.elements}
        return LegoPart(**data)

class TemplateMinifigureRepoManager(BaseRepoManager):
    table = TEMPLATE_MINIFIGURE_TABLE

    def _to_record(self, template: TemplateMinifigure) -> Record:
        elemets = []
        for attr in self.table.attributes:
            value = getattr(template, attr.name)
            elemets.append(Element(attribute=attr, value=value))

class ActualMinifigureRepoManager(BaseRepoManager):
    table = ACTUAL_MINIFIGURE_TABLE

class WeaponRepoManager:
    table = WEAPON_TABLE