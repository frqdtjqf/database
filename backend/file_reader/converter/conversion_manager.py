from backend.lego_db import LegoDBInterface, BasicModel, LegoPart
from backend.lego_db.db_converter import BaseRepoManager, LegoPartRepoManager

class BaseConversionManager:
    repo_mng : BaseRepoManager

    def __init__(self, db):
        self.repo_mng = BaseRepoManager(db)

    def model_from_dict(self, data: dict, name_conversion: dict[str, str]) -> BasicModel:
        model_dict = {}
        for key, value in data.items():
            model_dict[name_conversion[key]] = value

class LegoPartConversionManager:
    
    def __init__(self, db):
        self.repo_mng = LegoPartRepoManager(db)

    def model_from_dict(self, data: dict, name_conversion: dict[str, str]) -> LegoPart:
        pass