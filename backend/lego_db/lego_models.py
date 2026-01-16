"""
Dataclasses for Lego models."""

from dataclasses import dataclass, field, fields, Field
import hashlib
from typing import Mapping


UNDEFINED = object()

@dataclass(frozen=True)
class BasicModel:
    id: str = field(init=False, metadata={"super_id": True})

    def __post_init__(self):
        missing = []
        for f in self.creation_fields():
            value = getattr(self, f.name, None)

            if isinstance(value, str):
                trimmed = value.strip()
                if trimmed != value:
                    object.__setattr__(self, f.name, trimmed)

            if value is None or (isinstance(value, str) and value.strip() == ""):
                missing.append(f.name)
        if missing:
            raise ValueError(f"Missing required creation fields: {missing}")
        
        object.__setattr__(self, "id", self.compute_id())

    def compute_id(self) -> str:
        base = self.id_source()
        digest = hashlib.sha256(base.encode()).hexdigest()
        return digest[:16]
    
    def id_source(self) -> str:
        """gibt einzigartigen string zurück, aus welchem dann die id erstellt wird"""
        raise NotImplementedError("id_source missing implementation")
    
    @classmethod
    def creation_fields(cls) -> list[Field]:
        return [
            f for f in fields(cls)
            if f.metadata.get("id_field", False)
        ]

# Lego Teil
@dataclass(frozen=True)
class LegoPart(BasicModel):
    bricklink_part_id: str = field(metadata={"id_field": True})
    bricklink_color_id: str = field(metadata={"id_field": True})

    lego_element_id: str = ""
    lego_design_id: str = ""

    description: str = ""

    def id_source(self) -> str:
        return f"{self.bricklink_part_id}_{self.bricklink_color_id}"

# Waffentypen für Minifiguren
@dataclass(frozen=True)
class Weapon(BasicModel):
    name: str = field(metadata={"id_field": True})
    parts: Mapping[LegoPart, int] = field(default_factory=dict, metadata={"id_field": True, "related_field": True, "repo": "lego_part", "map": True})
    description: str = ""

    def id_source(self) -> str:
        base = self.name
        for part in sorted(self.parts, key=lambda p: p.id):
            count = self.parts[part]
            base += f"_{part.id}x{count}"
        return base

# eine Waffenauswahl für Minifiguren
@dataclass(frozen=True)
class WeaponSlot(BasicModel):
    weapons: Mapping[Weapon, int] = field(default_factory=dict, metadata={"id_field": True, "related_field": True, "repo": "weapon", "map": True})

    def id_source(self) -> str:
        if not self.weapons:
            return "empty_slot"

        base = "ws"
        for weapon in sorted(self.weapons, key=lambda w: w.id):
            count = self.weapons[weapon]
            base += f"_{weapon.id}x{count}"
        return base

# eine Lego Minifigur zusammengesetzt aus verschiedenen Teilen
@dataclass(frozen=True)
class TemplateMinifigure(BasicModel):
    bricklink_fig_id: str = field(metadata={"id_field": True})
    name: str
    year: str
    sets: frozenset[str] = field(default_factory=frozenset, metadata={"set": True})

    parts: Mapping[LegoPart, int] = field(default_factory=dict, metadata={"related_field": True, "repo": "lego_part", "map": True})
    possible_weapons: Mapping[WeaponSlot, int] = field(default_factory=dict, metadata={"related_field": True, "repo": "weapon_slot", "map": True})
    description: str = ""

    def id_source(self) -> str:
        return self.bricklink_fig_id

# eine reale Lego Minifigur im Bestand
@dataclass(frozen=True)
class ActualMinifigure(BasicModel):
    template: TemplateMinifigure = field(metadata={"related_field": True, "repo": "template", "set": False})

    box_number: str = field(metadata={"id_field": True})
    position_in_box: str = field(metadata={"id_field": True})

    weapon_slot: WeaponSlot = field(default_factory=lambda: WeaponSlot(), metadata={"related_field": True, "repo": "weapon_slot", "set": False})
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
        base = f"{self.box_number}_{self.position_in_box}"
        return base