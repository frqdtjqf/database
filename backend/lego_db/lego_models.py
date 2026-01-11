"""
Dataclasses for Lego models."""

from dataclasses import dataclass

# Lego Teil
@dataclass
class LegoPart:
    id: str
    color: str
    description: str = ""

# Waffentypen für Minifiguren
@dataclass(frozen=True)
class Weapon:
    id: str
    name: str
    parts: frozenset[LegoPart]
    description: str = ""

# eine Waffenauswahl für Minifiguren
@dataclass(frozen=True)
class WeaponSlot:
    weapons: frozenset[Weapon]

# eine Lego Minifigur zusammengesetzt aus verschiedenen Teilen
@dataclass(frozen=True)
class TemplateMinifigure:
    id: str
    name: str
    year: int
    sets: frozenset[str]
    possible_weapons: frozenset[WeaponSlot] | None = None
    description: str = ""

# eine reale Lego Minifigur im Bestand
@dataclass
class ActualMinifigure:
    id: str
    template: TemplateMinifigure

    box_number: int
    position_in_box: int

    weaponSlot: WeaponSlot | None = None
    condition: str = ""

    def __post_init__(self):
        self.validate_weapon()

    def validate_weapon(self) -> bool:
        """Validate that the assigned weapon is allowed for the template."""
        if self.weaponSlot is None:
            return True
        if self.template.possible_weapons is None:
            raise ValueError(f"Template {self.template.name} does not allow any weapons, but weapon {self.weaponSlot.weapons} was assigned.")
        if self.weaponSlot not in self.template.possible_weapons:
            raise ValueError(f"Weapon {self.weaponSlot.weapons} is not allowed for template {self.template.name}.")
        return True

