from backend.lego_db.lego_models import LegoPart, TemplateMinifigure, Weapon, ActualMinifigure
from backend.sql_api import DataBaseWrapper, Table
from backend.lego_db.db_converter import LegoDBConverter

class LegoDBInterface:

    def __init__(self, db: DataBaseWrapper, converter: LegoDBConverter):
        self.db = db
        self.converter = converter

    def create_tables(self, tables: list[Table]):
        for table in tables:
            self.db.create_table(table)

    def insert_models(self, legoModels: list[LegoPart|TemplateMinifigure|ActualMinifigure|Weapon], table: Table):
        for model in legoModels:
            record = self.converter.legomodel_to_dbrecord(model, table)
            self.db.insert_record(table, record)

    def get_models(self, table: Table) -> list[LegoPart|TemplateMinifigure|ActualMinifigure|Weapon]:
        models = []
        records = self.db.get_records(table)

        for record in records:
            model = self.converter.dbrecord_to_legomodel(record, table)
            models.append(model)
        return models
    
    def delete_table(self, table: Table):
        self.db.delete_table(table)

    def delete_models(self, table: Table, legoModels: list[LegoPart|TemplateMinifigure|ActualMinifigure|Weapon]):
        for model in legoModels:
            record = self.converter.legomodel_to_dbrecord(model, table)
            self.db.delete_record(table, record)