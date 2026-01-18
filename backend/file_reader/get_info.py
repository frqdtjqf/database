from backend.file_reader.read_file import read_csv
from backend.file_reader.converter.conversion_manager import BaseConversionManager
from backend.lego_db import LegoDBInterface, BasicModel

def csv_converter(mng: BaseConversionManager, csv_data: list[dict]) -> list[BasicModel]:
    models : list[BasicModel] = []

    for row in csv_data:
        try:
            model = mng.model_from_dict(row)
            mng.repo_mng.add_model(model)
        except Exception as e:
            print(f"Data could not be parsed in row {row}: {e}")

    return models

def import_csv(file):
    return read_csv(file)