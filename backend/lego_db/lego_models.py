"""
Dataclasses for Lego models."""

from dataclasses import dataclass
from enum import Enum

# verschiedene Accessory Typen
class AccessoryType(Enum):
    WEAPON = "weapon"
    TOOL = "tool"
    CAPE = "cape"
    HEADGEAR = "headgear"
    OTHER = "other"

class SlotType(Enum):
    HEADGEAR = "headgear"
    HANDHELD = "handheld"
    BACKPACK = "backpack"
    BELT = "belt"
    OTHER = "other"

# indivudiuelle Lego Teile
@dataclass(frozen=True)
class Part:
    id: str
    color: str
    description: str = ""

# optionale Accessoires für Minifiguren
@dataclass(frozen=True)
class Accessory:
    name: str
    type: AccessoryType
    parts: list[Part]
    description: str = ""

@dataclass(frozen=True)
class AccessorySlot:
    type: SlotType
    possible_accessories: list[Accessory]
    required: bool = False

# eine Lego Minifigur zusammengesetzt aus verschiedenen Teilen
@dataclass(frozen=True)
class TheoreticalMinifigure:
    id: str
    name: str
    year: int
    sets: list[str]

    parts: list[Part]

    headgear: Accessory | None = None
    accessories: list[AccessorySlot]
    description: str = ""

# eine reale Lego Minifigur im Bestand
@dataclass
class PhysicalMinifigure:
    id: str
    template: TheoreticalMinifigure

    # tatsächliche Accessories: Liste von (Slot, Accessory | None)
    accessories: list[tuple[AccessorySlot, Accessory | None]]

    # storage info
    box_number: int
    position_in_box: int

    condition: str = ""

    def validate(self) -> bool:
        """
        Stellt sicher, dass 
        1. alle required Accessories vorhanden sind (aber nicht belegte required Slots werden ignoriert).
        2. keine unzulässigen Accessories vorhanden sind.
        3. Jeder Slot ist nur einmal belegt.
        """
        slots_used = []
        for slot, acc in self.accessories:

            # 3. Prüfe doppelte Slots
            if slot in slots_used:
                raise ValueError(f"Slot {slot.type} is assigned multiple times for minifigure {self.id}")
            slots_used.append(slot)
            
            # 2.Check ob Accessory erlaubt ist
            if acc is not None:
                if acc not in slot.possible_accessories:
                    raise ValueError(f"Accessory {acc.name} is not allowed for slot {slot.type} in minifigure {self.id}")
                
            # 1. Check ob None Slot required ist
            else:
                if slot.required:
                    raise ValueError(f"Required slot {slot.type} is not filled for minifigure {self.id}")
        
        return True

