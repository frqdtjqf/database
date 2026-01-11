import csv
import json

def read_csv_file(file_path: str) -> list[dict[str, str]]:
    """Reads a CSV file and returns a list of dictionaries representing the rows."""
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]
    
def read_json_file(file_path: str) -> dict:
    """Reads a JSON file and returns its content as a dictionary."""
    with open(file_path, mode='r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        return data