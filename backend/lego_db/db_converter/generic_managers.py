from backend.lego_db.lego_models import LegoPart, TemplateMinifigure, ActualMinifigure, Weapon, WeaponSlot, BasicModel
from backend.sql_api import Table, Record, Element
from backend.lego_db.db_converter.registry import RELATIONS, QUANTITY
from backend.sql_api import DataBaseWrapper
from typing import Mapping

# Klasse für Models ohne Child oder mit einer 1:1 Beziehung
class BaseRepoManager:
    table: Table
    model_cls: type[BasicModel]
    joint_tables: list[Table]

    def __init__(self, db: DataBaseWrapper):
        self.db = db

    def get_model_ids(self) -> list[str]:
        mids = []
        models = self.get_models()
        for model in models:
            mids.append(model.id)
        return mids

    # --- Write Models ---
    # Spaltet das Model in mehrere Reports welche dann in die Tabellen geschrieben werden
    def add_model(self, model: BasicModel):
        record = self._record_from_model(model)
        self.db.insert_record(self.table, record)

    def delete_model(self, model: BasicModel):
        record = self._record_from_model(model)
        self.db.delete_record(self.table, record)

    # --- Read Models ---
    # Sammelt Models für eine Tabelle
    def get_models(self) -> list[BasicModel]:
        records = self.db.get_records(self.table)
        return [self._model_from_record(record) for record in records]

    # --- Table Management ---
    def delete_tables(self):
        for joint_tab in self.joint_tables:
            self.db.delete_table(joint_tab)
        self.db.delete_table(self.table)

    def create_tables(self):
        self.db.create_table(self.table)

    # --- Helpers ---
    def get_model_by_primary_key(self, pk_value: str) -> BasicModel:
        models = self.get_models()
        for model in models:
            record = self._record_from_model(model)
            pk_element = record.get_primary_key_element()
            if pk_element.value == pk_value:
                return model
            
    # --- Generic Conversion  ---
    # schreibt genau einen Record für eine Tabelle
    # row from Model
    def _record_from_model(self, model) -> Record:
        elements = []
        for attr in self.table.attributes:
            value = getattr(model, attr.name)
            elements.append(Element(attr, value))
        return Record(elements=elements)

    
    # sammelt Records aus Tabellen, um das Model wieder zu bauen
    # Model from row
    def _model_from_record(self, record: Record) -> BasicModel:
        raise NotImplementedError

# Klasse für alle Models, welche eine N:M beziehung mit ihren Childs haben
class ParentRepoManager(BaseRepoManager):
    def _load_related_models(
            self,
            relation_name: str,
            child_manager: BaseRepoManager,
            parent_id: str
    ) -> Mapping[BasicModel, int]:
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
        child_quantity_attribute = joint_table.get_attribute_by_name(QUANTITY)

        # Alle records mit der parent_id in der entsprechenden Spalte
        records = self.db.get_query_records(joint_table, joint_table_parent_attribute, parent_id)

        results: dict[BasicModel, int] = {}
        
        # jetzt child_ids aus den records sammeln um Objekte zu rekonstruieren
        for r in records:
            child_id_element = r.get_element_by_attribute_name(joint_table_child_attribute_name)
            child_id = child_id_element.value
            
            if child_id is None:
                raise ValueError(f"No value found for attribute '{joint_table_child_attribute.name}' in record {r}")
            
            child_model = child_manager.get_model_by_primary_key(child_id)

            if child_model is None:
                raise ValueError(f"No model found in table '{child_manager.table.name}' with id '{child_id}'")
            
            quantity = r.get_element_by_attribute_name(child_quantity_attribute.name).value

            results[child_model] = quantity

        return results
    
    def add_model(self, model: BasicModel):
        # 1. haupt record in seine Tabelle einfügen
        super().add_model(model)
        # 2. relations hinzufügen
        self._persist_relations(model)

    def _persist_relations(self, model: BasicModel):
        """Override in subclass as needed"""
        # stellt die Brücke zwische add_model und add_relations
        raise NotImplementedError

    def _add_relations(
            self, 
            child_models: Mapping[BasicModel, int],
            child_manager: BaseRepoManager,
            relation_name: str,
            parent_id: str
    ):
        # Fügt die Werte in die Joint Tables ein
        relation = RELATIONS[relation_name]
        joint_table: Table = relation["joint_table"]
        joint_table_parent_attribute_name: str = relation["parent_column"]
        joint_table_child_attribute_name: str = relation["child_column"]

        for model, quantity in child_models.items():
            # add child model in its own Table
            child_manager.add_model(model)

            # add relation to respective joint Table
            joint_record = Record(
                elements=[
                    Element(
                        attribute=joint_table.get_attribute_by_name(joint_table_parent_attribute_name),
                        value=parent_id
                    ),
                    Element(
                        attribute=joint_table.get_attribute_by_name(joint_table_child_attribute_name),
                        value=model.id
                    ),
                    Element(
                        attribute=joint_table.get_attribute_by_name(QUANTITY),
                        value=quantity
                    )
                ]
            )

            self.db.insert_record(
                table=joint_table,
                record=joint_record
            )