from backend.sql_api import DataBaseWrapper, Table
from backend.lego_db.lego_models import LegoPart, TemplateMinifigure, Weapon, ActualMinifigure
from backend.lego_db.model_converter import dbrecord_to_legomodel

def read_models_from_table(db: DataBaseWrapper, table: Table) -> list[LegoPart|TemplateMinifigure|ActualMinifigure|Weapon]:
    models = []
    records = db.get_records(table)

    for record in records:
        model = dbrecord_to_legomodel(record, table)
        models.append(model)
    return models