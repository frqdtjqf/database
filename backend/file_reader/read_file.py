import csv
import io

def read_csv(file) -> list[dict[str, str]]:
    stream = io.StringIO(file.stream.read().decode("utf-8"))
    reader = csv.DictReader(stream)

    if not reader.fieldnames:
        raise ValueError("CSV hat keinen Header")

    rows: list[dict[str, str]] = []

    for row in reader:
        clean_row = {
            k.strip(): (v.strip() if v is not None else "")
            for k, v in row.items()
        }
        rows.append(clean_row)

    return rows
