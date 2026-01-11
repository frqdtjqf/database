import csv

def read_csv_file(file_path: str) -> list[dict[str, str]]:
    """Reads a CSV file and returns a list of dictionaries representing the rows."""
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]