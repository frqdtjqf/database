"""
Dataclasses for Lego models."""

from dataclasses import dataclass, field
import hashlib

UNDEFINED = object()

@dataclass(frozen=True)
class BasicElement:
    id: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "id", self.compute_id())

    def compute_id(self) -> str:
        base = self.id_source()
        digest = hashlib.sha256(base.encode()).hexdigest()
        return digest[:16]
    
    def id_source(self) -> str:
        raise NotImplementedError("id_source missing implementation")

# Lego Teil
@dataclass(frozen=True)
class LegoPart(BasicElement):
    bricklink_part_id: str
    bricklink_color_id: str

    lego_element_id: str | None = ""
    lego_design_id: str | None = ""

    description: str = ""

    def id_source(self) -> str:
        return f"{self.bricklink_part_id}_{self.bricklink_color_id}"

# Waffentypen für Minifiguren
@dataclass(frozen=True)
class Weapon(BasicElement):
    name: str
    parts: frozenset[LegoPart] = frozenset()
    description: str = ""

    def id_source(self) -> str:
        base = self.name
        part_ids = sorted(part.id for part in self.parts)
        for pid in part_ids:
            base += f"_{pid}"
        return base

# eine Waffenauswahl für Minifiguren
@dataclass(frozen=True)
class WeaponSlot(BasicElement):
    weapons: frozenset[Weapon] = frozenset()

    def id_source(self) -> str:
        if not self.weapons:
            return "empty_slot"

        weapon_ids = sorted(w.id for w in self.weapons)
        return "slot_" + "_".join(weapon_ids)

# eine Lego Minifigur zusammengesetzt aus verschiedenen Teilen
@dataclass(frozen=True)
class TemplateMinifigure(BasicElement):
    bricklink_fig_id: str
    name: str
    year: int
    sets: frozenset[str]

    parts: frozenset[LegoPart] = frozenset()
    possible_weapons: frozenset[WeaponSlot] = frozenset()
    description: str = ""

    def id_source(self) -> str:
        return self.bricklink_fig_id

# eine reale Lego Minifigur im Bestand
@dataclass(frozen=True)
class ActualMinifigure(BasicElement):
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

