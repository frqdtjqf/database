from backend.lego_db.lego_models import LegoPart, TemplateMinifigure, Weapon, ActualMinifigure
from backend.sql_api import DataBaseWrapper, Table
from backend.lego_db.model_converter import legomodel_to_dbrecord

def build_tables_from_json(db: DataBaseWrapper, tables: list[Table]):
    for table in tables:
        db.create_table(table)

def write_model_list_to_db(db: DataBaseWrapper, legoModels: list[LegoPart|TemplateMinifigure|ActualMinifigure|Weapon], table: Table):
    for model in legoModels:
        write_model_to_db(db, model, table)

def write_model_to_db(db: DataBaseWrapper, legoModel: LegoPart|TemplateMinifigure|ActualMinifigure|Weapon, table: Table):
    record = legomodel_to_dbrecord(legoModel, table)
    db.insert_record(table, record)

    