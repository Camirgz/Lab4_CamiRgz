"""
Sistema de armadura - Nueva funcionalidad para el laboratorio.
Implementa diferentes tipos de armadura con distintas mecánicas de absorción.
"""
from src.interfaces import Armor


class LeatherArmor(Armor):
    """Armadura de cuero - protección ligera."""
    
    def __init__(self, defense: int = 10):
        self._defense = defense
        self._durability = 100
    
    def get_defense(self) -> int:
        return self._defense
    
    def get_name(self) -> str:
        return "Leather Armor"
    
    def absorb_damage(self, incoming_damage: int) -> int:
        """
        Reduce el daño por un porcentaje fijo.
        """
        if self._durability <= 0:
            return incoming_damage
        
        absorbed = int(incoming_damage * 0.2)  # 20% de absorción
        self._durability = max(0, self._durability - 1)
        
        return max(0, incoming_damage - absorbed)


class PlateArmor(Armor):
    """Armadura de placas - protección pesada."""
    
    def __init__(self, defense: int = 30):
        self._defense = defense
        self._durability = 200
    
    def get_defense(self) -> int:
        return self._defense
    
    def get_name(self) -> str:
        return "Plate Armor"
    
    def absorb_damage(self, incoming_damage: int) -> int:
        """
        Reduce el daño significativamente, pero degrada más rápido.
        """
        if self._durability <= 0:
            return incoming_damage
        
        absorbed = int(incoming_damage * 0.5)  # 50% de absorción
        self._durability = max(0, self._durability - 2)
        
        return max(0, incoming_damage - absorbed)


class MagicShield(Armor):
    """Escudo mágico - protección adaptativa."""
    
    def __init__(self, defense: int = 20, mana: int = 100):
        self._defense = defense
        self._mana = mana
        self._max_mana = mana
    
    def get_defense(self) -> int:
        return self._defense
    
    def get_name(self) -> str:
        return "Magic Shield"
    
    def absorb_damage(self, incoming_damage: int) -> int:
        """
        Absorbe daño usando maná. La absorción mejora con más maná disponible.
        """
        if self._mana <= 0:
            return incoming_damage
        
        # Porcentaje de absorción basado en maná disponible
        mana_ratio = self._mana / self._max_mana
        absorption_rate = 0.3 + (mana_ratio * 0.4)  # 30-70% según maná
        
        absorbed = int(incoming_damage * absorption_rate)
        mana_cost = min(self._mana, absorbed // 2)
        self._mana = max(0, self._mana - mana_cost)
        
        return max(0, incoming_damage - absorbed)
    
    def recharge_mana(self, amount: int):
        """Recarga el maná del escudo."""
        self._mana = min(self._max_mana, self._mana + amount)
    
    def get_mana(self) -> int:
        """Retorna el maná actual."""
        return self._mana


class EnchantedArmor(Armor):
    """Armadura encantada - protección con efectos especiales."""
    
    def __init__(self, defense: int = 25):
        self._defense = defense
        self._durability = 150
        self._reflect_chance = 0.15  # 15% de chance de reflejar
        self._last_reflected = False
    
    def get_defense(self) -> int:
        return self._defense
    
    def get_name(self) -> str:
        return "Enchanted Armor"
    
    def absorb_damage(self, incoming_damage: int) -> int:
        """
        Absorbe daño y tiene chance de reflejar parte del mismo.
        """
        import random
        
        if self._durability <= 0:
            return incoming_damage
        
        # Chance de reflejar daño
        self._last_reflected = random.random() < self._reflect_chance
        
        if self._last_reflected:
            # Refleja 30% del daño y absorbe 40% adicional
            absorbed = int(incoming_damage * 0.7)
            self._durability = max(0, self._durability - 1)
            return max(0, incoming_damage - absorbed)
        else:
            # Absorción normal de 35%
            absorbed = int(incoming_damage * 0.35)
            self._durability = max(0, self._durability - 1)
            return max(0, incoming_damage - absorbed)
    
    def did_reflect(self) -> bool:
        """Verifica si el último ataque fue reflejado."""
        return self._last_reflected


class DummyArmor(Armor):
    """Armadura dummy para testing."""
    
    def __init__(self, defense: int = 5, absorption_rate: float = 0.1):
        self._defense = defense
        self._absorption_rate = absorption_rate
        self.damage_received_count = 0
    
    def get_defense(self) -> int:
        return self._defense
    
    def get_name(self) -> str:
        return "Dummy Armor"
    
    def absorb_damage(self, incoming_damage: int) -> int:
        """Absorbe un porcentaje fijo del daño."""
        self.damage_received_count += 1
        absorbed = int(incoming_damage * self._absorption_rate)
        return max(0, incoming_damage - absorbed)