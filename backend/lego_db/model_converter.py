from backend.lego_db.lego_models import LegoPart, TemplateMinifigure, ActualMinifigure, Weapon
from backend.sql_api import Table, Record, Element
from backend.lego_db.constants import MODEL_REGISTRY

def legomodel_to_dbrecord(legoModel: LegoPart|TemplateMinifigure|ActualMinifigure|Weapon, table: Table) -> Record:
    elements = []
    for attr in table.attributes:
        value = getattr(legoModel, attr.name)
        elements.append(Element(value=value, attribute=attr))
    return Record(elements=elements)

def dbrecord_to_legomodel(record: Record, table: Table) -> LegoPart|TemplateMinifigure|ActualMinifigure|Weapon:
    model_data = {}
    for element in record.elements:
        model_data[element.attribute.name] = element.value

    model_type = _get_class_type_for_table(table)
    return model_type(**model_data)
    
def _get_class_type_for_table(table: Table):
    try:
        model_type = MODEL_REGISTRY[table.name]
    except KeyError:
        raise ValueError(f"Unknown model type: {table.name}")
    return model_type