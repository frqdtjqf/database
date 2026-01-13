"""
Dataclasses for Lego models."""

from dataclasses import dataclass, field
import hashlib

UNDEFINED = object()

@dataclass(frozen=True)
class BasicModel:
    id: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "id", self.compute_id())

    def compute_id(self) -> str:
        base = self.id_source()
        digest = hashlib.sha256(base.encode()).hexdigest()
        return digest[:16]
    
    def id_source(self) -> str:
        """gibt einzigartigen string zurück, aus welchem dann die id erstellt wird"""
        raise NotImplementedError("id_source missing implementation")
    
    def get_column_row_data(self) -> tuple[list[str], dict[str, str]]:
        """definiert die Spalten und deren Inhalt eines Elements"""
        columns = ["ID"]
        rows = {columns[0]: self.id}
        return columns, rows


# Lego Teil
@dataclass(frozen=True)
class LegoPart(BasicModel):
    bricklink_part_id: str
    bricklink_color_id: str

    lego_element_id: str | None = ""
    lego_design_id: str | None = ""

    description: str = ""

    def id_source(self) -> str:
        return f"{self.bricklink_part_id}_{self.bricklink_color_id}"
    
    def get_column_row_data(self) -> tuple[list[str], dict[str, str]]:
        columns, rows = super().get_column_row_data()

        new_columns = ["BrickLink Part ID", "BrickLink Color ID", "Lego Element ID", "Lego Design ID", "Description"]
        rows.update({
            new_columns[0]: self.bricklink_part_id,
            new_columns[1]: self.bricklink_color_id,
            new_columns[2]: self.lego_element_id,
            new_columns[3]: self.lego_design_id,
            new_columns[4]: self.description
        })
        columns.extend(new_columns)
        return columns, rows

# Waffentypen für Minifiguren
@dataclass(frozen=True)
class Weapon(BasicModel):
    name: str
    parts: frozenset[LegoPart] = frozenset()
    description: str = ""

    def id_source(self) -> str:
        base = self.name
        part_ids = sorted(part.id for part in self.parts)
        for pid in part_ids:
            base += f"_{pid}"
        return base
    
    def get_column_row_data(self) -> tuple[list[str], dict[str, str]]:
        columns, rows = super().get_column_row_data()
        new_columns = ["Name", "Parts", "Description"]
        parts_str = ", ".join(part.id for part in self.parts)
        rows.update({
            new_columns[0]: self.name,
            new_columns[1]: parts_str,
            new_columns[2]: self.description
        })
        columns.extend(new_columns)
        return columns, rows

# eine Waffenauswahl für Minifiguren
@dataclass(frozen=True)
class WeaponSlot(BasicModel):
    weapons: frozenset[Weapon] = frozenset()

    def id_source(self) -> str:
        if not self.weapons:
            return "empty_slot"

        weapon_ids = sorted(w.id for w in self.weapons)
        return "slot_" + "_".join(weapon_ids)
    
    def get_column_row_data(self) -> tuple[list[str], dict[str, str]]:
        columns, rows = super().get_column_row_data()
        new_columns = ["Weapons"]
        weapons_str = ", ".join(weapon.id for weapon in self.weapons)
        rows.update({
            new_columns[0]: weapons_str
        })
        columns.extend(new_columns)
        return columns, rows

# eine Lego Minifigur zusammengesetzt aus verschiedenen Teilen
@dataclass(frozen=True)
class TemplateMinifigure(BasicModel):
    bricklink_fig_id: str
    name: str
    year: int
    sets: frozenset[str]

    parts: frozenset[LegoPart] = frozenset()
    possible_weapons: frozenset[WeaponSlot] = frozenset()
    description: str = ""

    def id_source(self) -> str:
        return self.bricklink_fig_id
    
    def get_column_row_data(self) -> tuple[list[str], dict[str, str]]:
        columns, rows = super().get_column_row_data()
        new_columns = ["BrickLink Figure ID", "Name", "Year", "Sets", "Parts", "Possible Weapon Slots", "Description"]
        sets_str = ", ".join(set_id for set_id in self.sets)
        parts_str = ", ".join(part.id for part in self.parts)
        posw_str = ", ".join(slot.id for slot in self.possible_weapons)
        rows.update({
            new_columns[0]: self.bricklink_fig_id,
            new_columns[1]: self.name,
            new_columns[2]: self.year,
            new_columns[3]: sets_str,
            new_columns[4]: parts_str,
            new_columns[5]: posw_str,
            new_columns[6]: self.description
        })
        columns.extend(new_columns)
        return columns, rows

# eine reale Lego Minifigur im Bestand
@dataclass(frozen=True)
class ActualMinifigure(BasicModel):
    template: TemplateMinifigure

    box_number: int
    position_in_box: int

    weapon_slot: WeaponSlot | None = WeaponSlot(frozenset())
    condition: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.validate_weapon()

    def validate_weapon(self) -> bool:
        """Validate that the assigned weapon is allowed for the template."""
        if not self.weapon_slot.weapons:
            return True
        if not self.template.possible_weapons:
            raise ValueError(f"Template {self.template.name} does not allow any weapons, but weapon {self.weapon_slot.weapons} was assigned.")
        if self.weapon_slot not in self.template.possible_weapons:
            raise ValueError(f"Weapon {self.weapon_slot.weapons} is not allowed for template {self.template.name}.")
        return True

    def id_source(self) -> str:
        base = f"{self.template.id}_{self.box_number}_{self.position_in_box}"
        return base
    
    def get_column_row_data(self) -> tuple[list[str], dict[str, str]]:
        columns, rows = super().get_column_row_data()
        new_columns = ["Template ID", "Box Number", "Position Number", "Weapon Slot", "Condition"]
        rows.update({
            new_columns[0]: self.template.id,
            new_columns[1]: self.box_number,
            new_columns[2]: self.position_in_box,
            new_columns[3]: self.weapon_slot.id,
            new_columns[4]: self.condition
        })
        columns.extend(new_columns)
        return columns, rows

