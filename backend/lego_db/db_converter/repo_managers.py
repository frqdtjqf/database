from backend.lego_db.lego_models import LegoPart, TemplateMinifigure, ActualMinifigure, Weapon, WeaponSlot
from backend.sql_api import Record, Element
from backend.lego_db.db_converter.registry import *
from backend.lego_db.db_converter.generic_managers import ParentRepoManager, BaseRepoManager

# ==== BASIC ====
# basic Managers with max. 1:1 relations that dont require an extra Table
class LegoPartRepoManager(BaseRepoManager):
    table = LEGO_PART_TABLE
    
    def _model_from_record(self, record: Record) -> LegoPart:
        data = {e.attribute.name: e.value for e in record.elements}
        return LegoPart(**data)
    
class ActualMinifigureRepoManager(BaseRepoManager):
    table = ACTUAL_MINIFIGURE_TABLE

    def __init__(self, db):
        super().__init__(db)
        self.template_manager = TemplateMinifigureRepoManager(db)

    def _model_from_record(self, record: Record) -> ActualMinifigure:
        data = {e.attribute.name: e.value for e in record.elements}

        template = self.template_manager.get_model_by_primary_key(data[TEMPLATE_NAME])

        data["template"] = template

        return ActualMinifigure(**data)

    def _record_from_model(self, model: ActualMinifigure) -> Record:
        elements = []
        for attr in self.table.attributes:
            if attr.name == TEMPLATE_NAME:
                value = model.template.id
            else:
                value = getattr(model, attr.name)
            elements.append(Element(attribute=attr, value=value))
        return Record(elements=elements)
    
# ==== PARENT ====
# parent Managers with arbitrary relations N:M, that require an extra Table
class WeaponSlotRepoManager(ParentRepoManager):
    # needed constants
    table = WEAPON_SLOT_TABLE
    wsw = WEAPON_SLOT_WEAPONS_JOINT

    def __init__(self, db):
        super().__init__(db)
        self.weapon_manager = WeaponRepoManager(db)
    
    def _model_from_record(self, record: Record) -> WeaponSlot:
        data = {e.attribute.name: e.value for e in record.elements}
        slot_id = data[PRIMARY_KEY_NAME]

        weapons = self._load_related_models(self.wsw, self.weapon_manager, slot_id)

        data["weapons"] = weapons
        return WeaponSlot(**data)
    
    def _persist_relations(self, model: WeaponSlot):
        self._add_relations(model.weapons, self.weapon_manager, self.wsw, model.id)

class TemplateMinifigureRepoManager(ParentRepoManager):
    # needed constants
    table = TEMPLATE_MINIFIGURE_TABLE
    tp = TEMPLATE_PARTS_JOINT
    tws = TEMPLATE_WEAPON_SLOTS_JOINT

    def __init__(self, db):
        super().__init__(db)
        self.part_manager = LegoPartRepoManager(db)
        self.weapon_slot_manager = WeaponSlotRepoManager(db)

    def _model_from_record(self, record: Record) -> TemplateMinifigure:
        data = {e.attribute.name: e.value for e in record.elements}
        template_id = data["id"]

        # 1) --- > TODO: load parts from TEMPLATE_MINIFIGURE_PART_TABLE
        parts = self._load_related_models(self.tp, self.part_manager, template_id)

        # 2) --- > TODO: load weaponSlots from TEMPLATE_MINIFIGURE_WEAPON_SLOT_TABLE
        possible_weapons = self._load_related_models(self.tws, self.weapon_slot_manager, template_id)

        data["parts"] = parts
        data["possible_weapons"] = possible_weapons

        return TemplateMinifigure(**data)
    
    def _record_from_model(self, model: TemplateMinifigure):
        elements = []
        for attr in self.table.attributes:
            value = getattr(model, attr.name)
            if attr.name == "sets":
                value = ",".join(sorted(value))  # serialize
            elements.append(Element(attr, value))
        return Record(elements=elements)
    
    def _persist_relations(self, model: TemplateMinifigure):
        self._add_relations(model.parts, self.part_manager, self.tp, model.id)
        self._add_relations(model.possible_weapons, self.weapon_slot_manager, self.tws, model.id)

class WeaponRepoManager(ParentRepoManager):
    # needed constants
    table = WEAPON_TABLE
    wp = WEAPON_PARTS_JOINT

    def __init__(self, db):
        super().__init__(db)
        self.part_manager = LegoPartRepoManager(db)

    def _model_from_record(self, record: Record) -> Weapon:
        data = {e.attribute.name: e.value for e in record.elements}
        weapon_id = data[PRIMARY_KEY_NAME]

        # TODO: load parts from WEAPON_PART_TABLE
        parts = self._load_related_models(self.wp, self.part_manager, weapon_id)

        data["parts"] = parts

        return Weapon(**data)
    
    def _persist_relations(self, model: Weapon):
        self._add_relations(model.parts, self.part_manager, self.wp, model.id)