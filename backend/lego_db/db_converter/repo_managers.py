from backend.lego_db.lego_models import LegoPart, TemplateMinifigure, ActualMinifigure, Weapon, WeaponSlot
from backend.sql_api import Table, Record, Element
from backend.lego_db.db_converter.registry import LEGO_PART_TABLE, WEAPON_TABLE, WEAPON_SLOT_TABLE, TEMPLATE_MINIFIGURE_TABLE, ACTUAL_MINIFIGURE_TABLE, RELATIONS
from backend.sql_api import DataBaseWrapper

# Klasse für Models ohne Child oder mit einer 1:1 Beziehung
class BaseRepoManager:
    table: Table

    def __init__(self, db: DataBaseWrapper):
        self.db = db

    # --- Write Models ---
    def add_model(self, model: LegoPart|TemplateMinifigure|ActualMinifigure|Weapon|WeaponSlot):
        record = self._to_record(model)
        self.db.insert_record(self.table, record)

    def delete_model(self, model: LegoPart|TemplateMinifigure|ActualMinifigure|Weapon|WeaponSlot):
        record = self._to_record(model)
        self.db.delete_record(self.table, record)

    # --- Read Models ---
    def get_models(self) -> list[LegoPart|TemplateMinifigure|ActualMinifigure|Weapon|WeaponSlot]:
        records = self.db.get_records(self.table)
        return [self._from_record(record) for record in records]

    # --- Table Management ---
    def delete_table(self):
        self.db.delete_table(self.table)

    def create_table(self):
        self.db.create_table(self.table)

    # --- Helpers ---
    def get_model_by_primary_key(self, pk_value: str) -> LegoPart|TemplateMinifigure|ActualMinifigure|Weapon|WeaponSlot | None:
        models = self.get_models()
        for model in models:
            record = self._to_record(model)
            pk_element = record.get_primary_key_element()
            if pk_element.value == pk_value:
                return model
            
    # --- Generic Conversion  ---
    def _to_record(self, model: LegoPart|TemplateMinifigure|ActualMinifigure|Weapon|WeaponSlot) -> Record:
        return Record(elements=[
            Element(attr, getattr(model, attr.name)) for attr in self.table.attributes
        ])
    
    def _from_record(self, record: Record) -> LegoPart|TemplateMinifigure|ActualMinifigure|Weapon|WeaponSlot:
        raise NotImplementedError

# Klasse für alle Models, welche eine N:M beziehung mit ihren Childs haben
class ParentRepoManager(BaseRepoManager):
    def _load_related_models(
            self,
            relation_name: str,
            child_manager: BaseRepoManager,
            parent_id: str
    ) -> frozenset:
        """
        Funktion wird vom Parent ausgeführt
        PARAMS:
            realtion_name: str                              relation_name aus Registry
            child_manager: BaseRepoManager                  RepoManager für die Child Tabelle
            parent_id: str                                  die ID (oft primary Key) vom Parent
        RETURNS:
            frozenset mit Objekten vom Child, welche laud joint_table zu der parent_id gemappt wurden  
        """
        relation = RELATIONS[relation_name]

        joint_table: Table = relation["joint_table"]
        joint_table_parent_attribute_name: str = relation["parent_column"]
        joint_table_child_attribute_name: str = relation["child_column"]

        joint_table_parent_attribute = joint_table.get_attribute_by_name(joint_table_parent_attribute_name)
        joint_table_child_attribute = joint_table.get_attribute_by_name(joint_table_child_attribute_name)

        # Alle records mit der parent_id in der entsprechenden Spalte
        records = self.db.get_query_records(joint_table, joint_table_parent_attribute, parent_id)

        results = set()
        
        # jetzt child_ids aus den records sammeln um Objekte zu rekonstruieren
        for r in records:
            child_id_element = r.get_element_by_attribute_name(joint_table_child_attribute_name)
            child_id = child_id_element.value
            
            if child_id is None:
                raise ValueError(f"No value found for attribute '{joint_table_child_attribute.name}' in record {r}")
            
            child_model = child_manager.get_model_by_primary_key(child_id)

            if child_model is None:
                raise ValueError(f"No model found in table '{child_manager.table.name}' with id '{child_id}'")
            
            results.add(child_model)

        return frozenset(results)

class WeaponSlotRepoManager(ParentRepoManager):
    table = WEAPON_SLOT_TABLE
    
    def _from_record(self, record: Record) -> WeaponSlot:
        data = {e.attribute.name: e.value for e in record.elements}
        slot_id = data["id"]

        weapon_manager = WeaponRepoManager(self.db)
        weapons = self._load_related_models("weapon_slot_weapons", weapon_manager, slot_id)

        data["weapons"] = weapons
        return WeaponSlot(**data)

class LegoPartRepoManager(BaseRepoManager):
    table = LEGO_PART_TABLE
    
    def _from_record(self, record: Record) -> LegoPart:
        data = {e.attribute.name: e.value for e in record.elements}
        return LegoPart(**data)

class TemplateMinifigureRepoManager(ParentRepoManager):
    table = TEMPLATE_MINIFIGURE_TABLE

    def _from_record(self, record: Record) -> TemplateMinifigure:
        data = {e.attribute.name: e.value for e in record.elements}
        template_id = data["id"]

        # 1) --- > TODO: load parts from TEMPLATE_MINIFIGURE_PART_TABLE
        part_manager = LegoPartRepoManager(self.db)
        parts = self._load_related_models("template_parts", part_manager, template_id)

        # 2) --- > TODO: load weaponSlots from TEMPLATE_MINIFIGURE_WEAPON_SLOT_TABLE
        weapon_slot_manager = WeaponSlotRepoManager(self.db)
        possible_weapons = self._load_related_models("template_weapon_slots", weapon_slot_manager, template_id)

        data["parts"] = parts
        data["possible_weapons"] = possible_weapons

        return TemplateMinifigure(**data)

class ActualMinifigureRepoManager(BaseRepoManager):
    table = ACTUAL_MINIFIGURE_TABLE

    def _from_record(self, record: Record) -> ActualMinifigure:
        data = {e.attribute.name: e.value for e in record.elements}

        template_manager = TemplateMinifigureRepoManager(self.db)
        template = template_manager.get_model_by_primary_key(data["template_id"])

        data["template"] = template

        return ActualMinifigure(**data)

    def _to_record(self, model: ActualMinifigure) -> Record:
        elements = []
        for attr in self.table.attributes:
            if attr.name == "template_id":
                value = model.template.id
            else:
                value = getattr(model, attr.name)
            elements.append(Element(attribute=attr, value=value))
        return Record(elements=elements)

class WeaponRepoManager(ParentRepoManager):
    table = WEAPON_TABLE

    def _from_record(self, record: Record) -> Weapon:
        data = {e.attribute.name: e.value for e in record.elements}
        weapon_id = data["id"]

        # TODO: load parts from WEAPON_PART_TABLE
        part_manager = LegoPartRepoManager(self.db)
        parts = self._load_related_models("weapon_parts", part_manager, weapon_id)

        data["parts"] = parts

        return Weapon(**data)