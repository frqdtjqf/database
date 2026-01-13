from backend.lego_db.db_converter import BaseRepoManager
from backend.sql_api import DataBaseWrapper
from frontend.api_managers.web_models import WebTable

class BaseWebManager:
    columns: list[str]
    rows: dict[str, str]
    t_name: str

    def __init__(self, db: DataBaseWrapper):
        self.repo_mng = BaseRepoManager(db)

    def get_columns(self) -> list[str]:
        return self.columns
    
    def get_rows(self) -> dict[str, str]:
        raise NotImplementedError("get_rows not implemented")
    
    def get_web_table(self) -> WebTable:
        return WebTable(
            name=self.t_name,
            columns=self.get_columns(),
            rows=self.get_rows()
        )