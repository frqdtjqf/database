from backend.lego_db.lego_models import LegoPart, Weapon, WeaponSlot, TemplateMinifigure
from backend.lego_db.csv_versions.get_csv_versions import get_csv_part_versions

def read_lego_parts(data : list[dict[str, str]], version_name: str) -> list[LegoPart]:
    version = get_csv_part_versions(version_name)
    parts = []
    for row in data:
        id = row.get(version.id)
        color = row.get(version.color)
        description = row.get(version.description, "")
        
        part = LegoPart(
            id=id,
            color=color,
            description=description
        )
        parts.append(part)
    return parts

def read_template_minifigures(data : list[dict[str, str]], version_name: str) -> list[TemplateMinifigure]:
    version = get_csv_part_versions(version_name)
    minifigures = []
    for row in data:
        id = row.get(version.id)
        name = row.get(version.name)
        year = int(row.get(version.year))
        sets = frozenset(row.get(version.sets).split(version.seperator))
        description = row.get(version.description, "")

        minifigure = TemplateMinifigure(
            id=id,
            name=name,
            year=year,
            sets=sets,
            description=description
        )
        minifigures.append(minifigure)
    return minifigures