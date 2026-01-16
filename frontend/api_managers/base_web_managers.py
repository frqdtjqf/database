from backend.lego_db.db_converter import BaseRepoManager
from backend.lego_db.lego_models import BasicModel
from backend.sql_api import DataBaseWrapper
from frontend.api_managers.web_models import WebTable
from dataclasses import fields
from typing import Mapping

class BaseWebManager:
    columns: list[str]
    rows: dict[str, str]
    t_name: str
    entity: str
    repos: dict[str, BaseRepoManager]

    def __init__(self, db: DataBaseWrapper):
        self.repo_mng = BaseRepoManager(db)

    def get_columns(self) -> list[str]:
        return self.columns
    
    def get_rows(self) -> list[dict[str, str]]:
        raise NotImplementedError("get_rows not implemented")
    
    def get_web_table(self) -> WebTable:
        return WebTable(
            entity=self.entity,
            name=self.t_name,
            columns=self.get_columns(),
            rows=self.get_rows()
        )
    
    def get_model_ids(self) -> list[str]:
        return self.repo_mng.get_model_ids()
    
    def create_model(self, data: dict):
        kwargs = {}

        for f in fields(self.repo_mng.model_cls):
            name = f.name
            meta = f.metadata

            if meta.get("super_id"):
                continue

            raw = None

            # ----------   SET  ----------
            if meta.get("set"):
                # multi values
                values = data.get(name, []) if isinstance(data[name], list) else [data.get(name, [])]
                values = [v for v in values if v != ""]
                raw = frozenset(values)
            # ---------- MAP ----------
            elif f.metadata.get("map"):
                # Mapping-Feld: Key+Value → dict
                keys = data.get(f"{f.name}_key", [])
                values = data.get(f"{f.name}_value", [])
                mapping = {}
                repo = self.repos[meta["repo"]]
                for k, v in zip(keys, values):
                    if (k is None) or (k==""):
                        continue
                    mapping[repo.get_model_by_primary_key(k)] = int(v)
                raw = mapping

            # ---------- NESTED ----------
            elif meta.get("related_field"):
                # single nested
                value = data.get(name)[0]
                if not value:
                    raw = None
                else:
                    repo = self.repos[meta["repo"]]
                    raw = repo.get_model_by_primary_key(value)
            # ---------- FLAT ----------
            else:
                # flat
                raw = data.get(name)[0]
                if raw == "":
                    raw = None
                if meta.get("id_field") and not raw:
                    raise ValueError(f"{name} missing")

            kwargs[name] = raw

        return self.repo_mng.model_cls(**kwargs)




