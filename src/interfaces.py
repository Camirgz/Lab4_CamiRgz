"""
Interfaces para el sistema de combate.
Estas interfaces siguen el principio de Dependency Inversion (SOLID).
"""
from abc import ABC, abstractmethod
from typing import Protocol


class Weapon(ABC):
    """Interfaz para armas en el sistema de combate."""
    
    @abstractmethod
    def get_damage(self) -> int:
        """Retorna el daño base del arma."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retorna el nombre del arma."""
        pass


class DamageCalculator(ABC):
    """Interfaz para calcular daño en combate."""
    
    @abstractmethod
    def calculate_damage(self, base_damage: int, attacker_level: int, defender_level: int) -> int:
        """
        Calcula el daño final considerando niveles.
        
        Args:
            base_damage: Daño base del arma
            attacker_level: Nivel del atacante
            defender_level: Nivel del defensor
            
        Returns:
            Daño final calculado
        """
        pass


class Armor(ABC):
    """Interfaz para sistema de armadura."""
    
    @abstractmethod
    def get_defense(self) -> int:
        """Retorna la defensa base de la armadura."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retorna el nombre de la armadura."""
        pass
    
    @abstractmethod
    def absorb_damage(self, incoming_damage: int) -> int:
        """
        Calcula el daño absorbido por la armadura.
        
        Args:
            incoming_damage: Daño entrante
            
        Returns:
            Daño después de la absorción
        """
        pass