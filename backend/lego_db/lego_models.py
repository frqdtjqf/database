"""
Dataclasses for Lego models."""

from dataclasses import dataclass, field, fields, Field
import hashlib

UNDEFINED = object()

@dataclass(frozen=True)
class BasicModel:
    id: str = field(init=False)

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

    lego_element_id: str | None = ""
    lego_design_id: str | None = ""

    description: str = ""

    def id_source(self) -> str:
        return f"{self.bricklink_part_id}_{self.bricklink_color_id}"

# Waffentypen für Minifiguren
@dataclass(frozen=True)
class Weapon(BasicModel):
    name: str = field(metadata={"id_field": True})
    parts: frozenset[LegoPart] = field(metadata={"id_field": True, "related_field": True})
    description: str = ""

    def id_source(self) -> str:
        base = "b"
        part_ids = sorted(part.id for part in self.parts)
        for pid in part_ids:
            base += f"_{pid}"
        return base

# eine Waffenauswahl für Minifiguren
@dataclass(frozen=True)
class WeaponSlot(BasicModel):
    weapons: frozenset[Weapon] = field(metadata={"id_field": True})

    def id_source(self) -> str:
        if not self.weapons:
            return "empty_slot"

        weapon_ids = sorted(w.id for w in self.weapons)
        return "slot_" + "_".join(weapon_ids)

# eine Lego Minifigur zusammengesetzt aus verschiedenen Teilen
@dataclass(frozen=True)
class TemplateMinifigure(BasicModel):
    bricklink_fig_id: str = field(metadata={"id_field": True})
    name: str
    year: int
    sets: frozenset[str] = field(default_factory=frozenset, metadata={"related_field": True})

    parts: frozenset[LegoPart] = field(default_factory=frozenset, metadata={"related_field": True})
    possible_weapons: frozenset[WeaponSlot] = field(default_factory=frozenset, metadata={"related_field": True})
    description: str = ""

    def id_source(self) -> str:
        return self.bricklink_fig_id

# eine reale Lego Minifigur im Bestand
@dataclass(frozen=True)
class ActualMinifigure(BasicModel):
    template: TemplateMinifigure = field(metadata={"related_field": True})

    box_number: int = field(metadata={"id_field": True})
    position_in_box: int = field(metadata={"id_field": True})

    weapon_slot: WeaponSlot = field(default_factory=lambda: WeaponSlot(frozenset()), metadata={"related_field": True})
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