from types import SimpleNamespace
from backend.file_reader.get_info import read_json_file

CSV_PATH = "/backend/lego_db/csv_versions/json"

PART_VERSIONS = "/csv_part_versions.json"
MINIFIGURE_VERSIONS = "/csv_minifigure_versions.json"

def get_csv_part_versions(version_name: str):
    data = read_json_file(f"{CSV_PATH}{PART_VERSIONS}")
    return SimpleNamespace(**data[version_name])

def get_csv_minifigure_versions(version_name: str):
    data = read_json_file(f"{CSV_PATH}{MINIFIGURE_VERSIONS}")
    return SimpleNamespace(**data[version_name])