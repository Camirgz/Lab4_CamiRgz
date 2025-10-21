"""
Sistema de combate principal.
Utiliza inyección de dependencias para ser fácilmente testeable.
"""
from src.interfaces import Weapon, DamageCalculator, Armor
from typing import Optional


class Character:
    """Representa un personaje en el combate."""
    
    def __init__(self, name: str, health: int, level: int, armor: Optional[Armor] = None):
        self.name = name
        self.max_health = health
        self.current_health = health
        self.level = level
        self.armor = armor
    
    def is_alive(self) -> bool:
        """Verifica si el personaje está vivo."""
        return self.current_health > 0
    
    def take_damage(self, damage: int) -> int:
        """
        Aplica daño al personaje.
        
        Args:
            damage: Daño a recibir
            
        Returns:
            Daño real recibido después de aplicar armadura
        """
        actual_damage = damage
        
        if self.armor:
            actual_damage = self.armor.absorb_damage(damage)
        
        self.current_health = max(0, self.current_health - actual_damage)
        return actual_damage
    
    def heal(self, amount: int):
        """Cura al personaje."""
        self.current_health = min(self.max_health, self.current_health + amount)
    
    def equip_armor(self, armor: Armor):
        """Equipa una armadura."""
        self.armor = armor


class CombatSystem:
    """
    Sistema de combate que utiliza inyección de dependencias.
    Esto permite cambiar el comportamiento sin modificar la clase.
    """
    
    def __init__(self, damage_calculator: DamageCalculator):
        """
        Inicializa el sistema de combate.
        
        Args:
            damage_calculator: Implementación del calculador de daño
        """
        self.damage_calculator = damage_calculator
        self.combat_log = []
    
    def attack(self, attacker: Character, defender: Character, weapon: Weapon) -> dict:
        """
        Ejecuta un ataque de un personaje a otro.
        
        Args:
            attacker: Personaje atacante
            defender: Personaje defensor
            weapon: Arma utilizada
            
        Returns:
            Diccionario con información del ataque
        """
        if not attacker.is_alive():
            return {
                "success": False,
                "message": f"{attacker.name} está muerto y no puede atacar"
            }
        
        if not defender.is_alive():
            return {
                "success": False,
                "message": f"{defender.name} ya está muerto"
            }
        
        # Calcular daño usando el calculador inyectado
        base_damage = weapon.get_damage()
        calculated_damage = self.damage_calculator.calculate_damage(
            base_damage,
            attacker.level,
            defender.level
        )
        
        # Aplicar daño al defensor (la armadura se maneja internamente)
        actual_damage = defender.take_damage(calculated_damage)
        
        # Registrar en log
        log_entry = (
            f"{attacker.name} (Lvl {attacker.level}) atacó a {defender.name} "
            f"(Lvl {defender.level}) con {weapon.get_name()} causando {actual_damage} daño"
        )
        self.combat_log.append(log_entry)
        
        return {
            "success": True,
            "attacker": attacker.name,
            "defender": defender.name,
            "weapon": weapon.get_name(),
            "damage": actual_damage,
            "defender_health": defender.current_health,
            "defender_alive": defender.is_alive(),
            "message": log_entry
        }
    
    def get_combat_log(self) -> list:
        """Retorna el log de combate."""
        return self.combat_log.copy()
    
    def clear_log(self):
        """Limpia el log de combate."""
        self.combat_log.clear()