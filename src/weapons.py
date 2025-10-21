"""
Implementaciones concretas de armas.
"""
from src.interfaces import Weapon


class Sword(Weapon):
    """Espada básica."""
    
    def __init__(self, damage: int = 50):
        self._damage = damage
    
    def get_damage(self) -> int:
        return self._damage
    
    def get_name(self) -> str:
        return "Sword"


class Bow(Weapon):
    """Arco."""
    
    def __init__(self, damage: int = 40):
        self._damage = damage
    
    def get_damage(self) -> int:
        return self._damage
    
    def get_name(self) -> str:
        return "Bow"


class MagicStaff(Weapon):
    """Báculo mágico con bonus por inteligencia."""
    
    def __init__(self, damage: int = 60, intelligence_bonus: int = 10):
        self._damage = damage
        self._intelligence_bonus = intelligence_bonus
    
    def get_damage(self) -> int:
        return self._damage + self._intelligence_bonus
    
    def get_name(self) -> str:
        return "Magic Staff"


class DummyWeapon(Weapon):
    """Arma dummy para testing."""
    
    def __init__(self, damage: int = 10):
        self._damage = damage
    
    def get_damage(self) -> int:
        return self._damage
    
    def get_name(self) -> str:
        return "Dummy Weapon"