"""
Dataclasses for Lego models."""

from dataclasses import dataclass, field
import hashlib

UNDEFINED = object()

# Lego Teil
@dataclass(frozen=True)
class LegoPart:
    id: str
    color: str
    description: str = ""

# Waffentypen für Minifiguren
@dataclass(frozen=True)
class Weapon:
    id: str
    name: str
    parts: frozenset[LegoPart] = frozenset()
    description: str = ""

# eine Waffenauswahl für Minifiguren
@dataclass(frozen=True)
class WeaponSlot:
    weapons: frozenset[Weapon] = frozenset()
    id: str = field(init=False)

    def __post_init__(self):
        # bypass frozen
        object.__setattr__(self, 'id', self.compute_id())

    def compute_id(self) -> str:
        """Compute a deterministic ID based on the contained weapons."""
        if not self.weapons:
            return "empty_slot"
        # Sort weapons by ID for consistency
        weapon_ids = sorted(w.id for w in self.weapons)
        concat = ",".join(weapon_ids)
        # Use a short hash for uniqueness
        return hashlib.sha256(concat.encode()).hexdigest()[:8]

# eine Lego Minifigur zusammengesetzt aus verschiedenen Teilen
@dataclass(frozen=True)
class TemplateMinifigure:
    id: str
    name: str
    year: int
    sets: frozenset[str]

    parts: frozenset[LegoPart] = frozenset()
    possible_weapons: frozenset[WeaponSlot] = frozenset()
    description: str = ""

# eine reale Lego Minifigur im Bestand
@dataclass(frozen=True)
class ActualMinifigure:
    template: TemplateMinifigure

    box_number: int
    position_in_box: int

    weaponSlot: WeaponSlot | None = None
    condition: str = ""
    id: str = field(init=False)

    def __post_init__(self):
        self.validate_weapon()
        object.__setattr__(self, 'id', self.compute_id())

    def validate_weapon(self) -> bool:
        """Validate that the assigned weapon is allowed for the template."""
        if self.weaponSlot is None:
            return True
        if self.template.possible_weapons is None:
            raise ValueError(f"Template {self.template.name} does not allow any weapons, but weapon {self.weaponSlot.weapons} was assigned.")
        if self.weaponSlot not in self.template.possible_weapons:
            raise ValueError(f"Weapon {self.weaponSlot.weapons} is not allowed for template {self.template.name}.")
        return True

    def compute_id(self) -> str:
        """Compute a deterministic ID based on position and template id"""
        unique_str = f"{self.template.id}_{self.box_number}_{self.position_in_box}"
        return hashlib.sha256(unique_str.encode()).hexdigest()[:8]

