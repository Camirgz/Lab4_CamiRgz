"""
Implementaciones de calculadores de daño.
"""
from src.interfaces import DamageCalculator


class StandardDamageCalculator(DamageCalculator):
    """Calculador estándar de daño."""
    
    def calculate_damage(self, base_damage: int, attacker_level: int, defender_level: int) -> int:
        """
        Fórmula: daño = base_damage * (1 + (attacker_level - defender_level) * 0.1)
        """
        level_difference = attacker_level - defender_level
        multiplier = 1 + (level_difference * 0.1)
        damage = int(base_damage * multiplier)
        return max(1, damage)  # Mínimo 1 de daño


class CriticalDamageCalculator(DamageCalculator):
    """Calculador con posibilidad de crítico."""
    
    def __init__(self, crit_multiplier: float = 2.0):
        self.crit_multiplier = crit_multiplier
        self.last_was_critical = False
    
    def calculate_damage(self, base_damage: int, attacker_level: int, defender_level: int) -> int:
        """
        Calcula daño con posibilidad de crítico basado en diferencia de nivel.
        """
        level_difference = attacker_level - defender_level
        
        # Probabilidad de crítico aumenta con nivel
        crit_chance = min(0.3, max(0.1, 0.1 + level_difference * 0.05))
        
        import random
        is_critical = random.random() < crit_chance
        self.last_was_critical = is_critical
        
        multiplier = 1 + (level_difference * 0.1)
        if is_critical:
            multiplier *= self.crit_multiplier
        
        damage = int(base_damage * multiplier)
        return max(1, damage)


class MockDamageCalculator(DamageCalculator):
    """Mock para testing."""
    
    def __init__(self, fixed_damage: int = 20):
        self.fixed_damage = fixed_damage
        self.call_count = 0
        self.last_base_damage = None
        self.last_attacker_level = None
        self.last_defender_level = None
    
    def calculate_damage(self, base_damage: int, attacker_level: int, defender_level: int) -> int:
        """Retorna daño fijo para pruebas predecibles."""
        self.call_count += 1
        self.last_base_damage = base_damage
        self.last_attacker_level = attacker_level
        self.last_defender_level = defender_level
        return self.fixed_damage