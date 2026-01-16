"""
Dataclasses for Lego models."""

from dataclasses import dataclass, field, fields, Field, MISSING
import hashlib
from typing import Mapping, Optional


UNDEFINED = object()

@dataclass(frozen=True)
class BasicModel:
    id: str = field(init=False, metadata={"super_id": True})

    def __post_init__(self):
        # Trim Strings + Requirements Check
        missing = []
        for f in self.creation_fields():
            value = getattr(self, f.name, None)

            if value is None:
                missing.append(f.name)
            elif isinstance(value, str) and value.strip() == "":
                missing.append(f.name)
            elif isinstance(value, (dict, list, set, frozenset)) and not value:
                missing.append(f.name)

        if missing:
            raise ValueError(f"Missing required creation fields: {missing}")
        
        # None -> default_factory
        for f in fields(self):
            if f.name == "id":
                continue

            value = getattr(self, f.name)

            if value is None:
                if f.default_factory is not MISSING:
                    object.__setattr__(self, f.name, f.default_factory())
        
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
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.id == other.id

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

    parts: Mapping[LegoPart, int] = field(default_factory=dict, metadata={"id_field": True, "related_field": True, "repo": "lego_parts", "map": True})
    description: str = ""

    def id_source(self) -> str:
        base = self.name
        for part in sorted(self.parts, key=lambda p: p.id):
            count = self.parts[part]
            base += f"_{part.id}x{count}"
        return base
    
    def __hash__(self):
        # hash based on name + sorted (LegoPart.id, count)
        parts_tuple = tuple(sorted((p.id, c) for p, c in self.parts.items()))
        return hash((self.name, parts_tuple))

    def __eq__(self, other):
        return isinstance(other, Weapon) and self.name == other.name and self.parts == other.parts

# eine Waffenauswahl für Minifiguren
@dataclass(frozen=True)
class WeaponSlot(BasicModel):
    weapons: Mapping[Weapon, int] = field(default_factory=dict, metadata={"id_field": True, "related_field": True, "repo": "weapons", "map": True})

    def id_source(self) -> str:
        if not self.weapons:
            return "empty_slot"

        base = "ws"
        for weapon in sorted(self.weapons, key=lambda w: w.id):
            count = self.weapons[weapon]
            base += f"_{weapon.id}x{count}"
        return base
    
    def __hash__(self):
        weapons_tuple = tuple(sorted((w.id, c) for w, c in self.weapons.items()))
        return hash(weapons_tuple)

    def __eq__(self, other):
        return isinstance(other, WeaponSlot) and self.weapons == other.weapons

# eine Lego Minifigur zusammengesetzt aus verschiedenen Teilen
@dataclass(frozen=True)
class TemplateMinifigure(BasicModel):
    bricklink_fig_id: str = field(metadata={"id_field": True})

    name: str = ""
    year: str = ""
    sets: frozenset[str] = field(default_factory=frozenset, metadata={"set": True})
    parts: Mapping[LegoPart, int] = field(default_factory=dict, metadata={"related_field": True, "repo": "lego_parts", "map": True})
    possible_weapons: Mapping[WeaponSlot, int] = field(default_factory=dict, metadata={"related_field": True, "repo": "weapon_slots", "map": True})
    description: str = ""

    def id_source(self) -> str:
        return self.bricklink_fig_id
    
    def __hash__(self):
        parts_tuple = tuple(sorted((p.id, c) for p, c in self.parts.items()))
        weapons_tuple = tuple(sorted((w.id, c) for w, c in self.possible_weapons.items()))
        return hash((self.bricklink_fig_id, parts_tuple, weapons_tuple))

    def __eq__(self, other):
        return (
            isinstance(other, TemplateMinifigure) and
            self.bricklink_fig_id == other.bricklink_fig_id and
            self.parts == other.parts and
            self.possible_weapons == other.possible_weapons
        )

# eine reale Lego Minifigur im Bestand
@dataclass(frozen=True)
class ActualMinifigure(BasicModel):
    box_number: str = field(metadata={"id_field": True})
    position_in_box: str = field(metadata={"id_field": True})

    template: TemplateMinifigure = field(metadata={"id_field": True, "related_field": True, "repo": "template_minifigures", "set": False})
    weapon_slot: Optional[WeaponSlot] = field(default=None, metadata={"related_field": True, "repo": "weapon_slots", "set": False})
    condition: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.validate_weapon()

    def validate_weapon(self) -> bool:
        """Validate that the assigned weapon is allowed for the template."""
        if not self.weapon_slot:
            return True
        elif not self.weapon_slot.weapons:
            return True
        elif not self.template.possible_weapons:
            raise ValueError(f"Template {self.template.name} does not allow any weapons, but weapon {self.weapon_slot.weapons} was assigned.")
        elif self.weapon_slot not in self.template.possible_weapons:
            raise ValueError(f"Weapon {self.weapon_slot.weapons} is not allowed for template {self.template.name}.")
        return True

    def id_source(self) -> str:
        base = f"{self.box_number}_{self.position_in_box}"
        return base
    
    def __hash__(self):
        return hash((self.box_number, self.position_in_box, self.template, self.weapon_slot))

    def __eq__(self, other):
        return (
            isinstance(other, ActualMinifigure) and
            self.box_number == other.box_number and
            self.position_in_box == other.position_in_box and
            self.template == other.template and
            self.weapon_slot == other.weapon_slot
        )