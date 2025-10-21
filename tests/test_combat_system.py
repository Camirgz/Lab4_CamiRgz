"""
Tests unitarios para el sistema de combate.
Demuestra el uso de inyección de dependencias y mocks.
"""
import unittest
from unittest.mock import Mock, MagicMock
from src.combat_system import CombatSystem, Character
from src.weapons import Sword, DummyWeapon
from src.damage_calculator import StandardDamageCalculator, MockDamageCalculator
from src.armor_system import LeatherArmor, DummyArmor


class TestCharacter(unittest.TestCase):
    """Tests para la clase Character."""
    
    def test_character_creation(self):
        """Verifica que un personaje se crea correctamente."""
        char = Character("Hero", 100, 5)
        self.assertEqual(char.name, "Hero")
        self.assertEqual(char.max_health, 100)
        self.assertEqual(char.current_health, 100)
        self.assertEqual(char.level, 5)
        self.assertTrue(char.is_alive())
    
    def test_character_take_damage(self):
        """Verifica que el personaje recibe daño correctamente."""
        char = Character("Hero", 100, 5)
        damage_dealt = char.take_damage(30)
        self.assertEqual(damage_dealt, 30)
        self.assertEqual(char.current_health, 70)
        self.assertTrue(char.is_alive())
    
    def test_character_death(self):
        """Verifica que el personaje muere al recibir daño letal."""
        char = Character("Hero", 50, 5)
        char.take_damage(60)
        self.assertEqual(char.current_health, 0)
        self.assertFalse(char.is_alive())
    
    def test_character_healing(self):
        """Verifica que el personaje se cura correctamente."""
        char = Character("Hero", 100, 5)
        char.take_damage(40)
        char.heal(20)
        self.assertEqual(char.current_health, 80)
    
    def test_character_healing_cap(self):
        """Verifica que la curación no excede el máximo de vida."""
        char = Character("Hero", 100, 5)
        char.take_damage(20)
        char.heal(50)
        self.assertEqual(char.current_health, 100)
    
    def test_character_with_armor(self):
        """Verifica que la armadura reduce el daño."""
        armor = DummyArmor(defense=10, absorption_rate=0.5)
        char = Character("Hero", 100, 5, armor=armor)
        
        damage_dealt = char.take_damage(40)
        self.assertEqual(damage_dealt, 20)  # 50% absorbido
        self.assertEqual(char.current_health, 80)


class TestCombatSystemWithDependencyInjection(unittest.TestCase):
    """
    Tests que demuestran inyección de dependencias.
    Podemos cambiar el comportamiento inyectando diferentes implementaciones.
    """
    
    def test_combat_with_standard_calculator(self):
        """Test con calculador estándar."""
        calculator = StandardDamageCalculator()
        combat = CombatSystem(calculator)
        
        attacker = Character("Knight", 100, 5)
        defender = Character("Goblin", 50, 3)
        weapon = Sword(damage=30)
        
        result = combat.attack(attacker, defender, weapon)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["attacker"], "Knight")
        self.assertEqual(result["defender"], "Goblin")
        self.assertGreater(result["damage"], 0)
    
    def test_combat_with_mock_calculator(self):
        """
        Test con calculador mock - daño predecible.
        Esto es útil para tests determinísticos.
        """
        mock_calculator = MockDamageCalculator(fixed_damage=25)
        combat = CombatSystem(mock_calculator)
        
        attacker = Character("Knight", 100, 5)
        defender = Character("Goblin", 50, 3)
        weapon = DummyWeapon(damage=20)
        
        result = combat.attack(attacker, defender, weapon)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["damage"], 25)
        self.assertEqual(defender.current_health, 25)
        
        # Verificar que el mock fue llamado correctamente
        self.assertEqual(mock_calculator.call_count, 1)
        self.assertEqual(mock_calculator.last_base_damage, 20)
    
    def test_combat_with_magic_mock(self):
        """Test usando MagicMock para verificar llamadas."""
        mock_calculator = MagicMock()
        mock_calculator.calculate_damage.return_value = 35
        
        combat = CombatSystem(mock_calculator)
        
        attacker = Character("Mage", 80, 7)
        defender = Character("Dragon", 200, 10)
        weapon = DummyWeapon(damage=40)
        
        result = combat.attack(attacker, defender, weapon)
        
        # Verificar que calculate_damage fue llamado
        mock_calculator.calculate_damage.assert_called_once_with(40, 7, 10)
        self.assertEqual(result["damage"], 35)
    
    def test_dead_attacker_cannot_attack(self):
        """Verifica que un atacante muerto no puede atacar."""
        calculator = StandardDamageCalculator()
        combat = CombatSystem(calculator)
        
        attacker = Character("Ghost", 0, 5)
        defender = Character("Hero", 100, 5)
        weapon = Sword()
        
        result = combat.attack(attacker, defender, weapon)
        
        self.assertFalse(result["success"])
        self.assertIn("muerto", result["message"].lower())
    
    def test_cannot_attack_dead_defender(self):
        """Verifica que no se puede atacar a un defensor muerto."""
        calculator = StandardDamageCalculator()
        combat = CombatSystem(calculator)
        
        attacker = Character("Knight", 100, 5)
        defender = Character("Skeleton", 0, 3)
        weapon = Sword()
        
        result = combat.attack(attacker, defender, weapon)
        
        self.assertFalse(result["success"])
        self.assertIn("muerto", result["message"].lower())
    
    def test_combat_log(self):
        """Verifica que el log de combate se registra correctamente."""
        calculator = MockDamageCalculator(fixed_damage=20)
        combat = CombatSystem(calculator)
        
        attacker = Character("Hero", 100, 5)
        defender = Character("Enemy", 100, 5)
        weapon = Sword()
        
        combat.attack(attacker, defender, weapon)
        combat.attack(attacker, defender, weapon)
        
        log = combat.get_combat_log()
        self.assertEqual(len(log), 2)
        
        combat.clear_log()
        self.assertEqual(len(combat.get_combat_log()), 0)
    
    def test_multiple_attacks_reduce_health(self):
        """Verifica múltiples ataques."""
        calculator = MockDamageCalculator(fixed_damage=15)
        combat = CombatSystem(calculator)
        
        attacker = Character("Warrior", 100, 5)
        defender = Character("Orc", 50, 5)
        weapon = DummyWeapon()
        
        # Primer ataque
        result1 = combat.attack(attacker, defender, weapon)
        self.assertEqual(defender.current_health, 35)
        self.assertTrue(result1["defender_alive"])
        
        # Segundo ataque
        result2 = combat.attack(attacker, defender, weapon)
        self.assertEqual(defender.current_health, 20)
        self.assertTrue(result2["defender_alive"])
        
        # Tercer ataque
        result3 = combat.attack(attacker, defender, weapon)
        self.assertEqual(defender.current_health, 5)
        self.assertTrue(result3["defender_alive"])
        
        # Cuarto ataque - mata al defensor
        result4 = combat.attack(attacker, defender, weapon)
        self.assertEqual(defender.current_health, 0)
        self.assertFalse(result4["defender_alive"])


class TestCombatWithArmor(unittest.TestCase):
    """Tests de combate con sistema de armadura."""
    
    def test_armor_reduces_damage(self):
        """Verifica que la armadura reduce el daño recibido."""
        calculator = MockDamageCalculator(fixed_damage=40)
        combat = CombatSystem(calculator)
        
        armor = LeatherArmor(defense=10)
        attacker = Character("Knight", 100, 5)
        defender = Character("Guard", 100, 5, armor=armor)
        weapon = Sword()
        
        result = combat.attack(attacker, defender, weapon)
        
        # La armadura de cuero absorbe 20%, así que debería recibir 32 de daño
        self.assertEqual(result["damage"], 32)
        self.assertEqual(defender.current_health, 68)
    
    def test_combat_without_armor_takes_full_damage(self):
        """Verifica que sin armadura se recibe todo el daño."""
        calculator = MockDamageCalculator(fixed_damage=40)
        combat = CombatSystem(calculator)
        
        attacker = Character("Knight", 100, 5)
        defender = Character("Peasant", 100, 5)
        weapon = Sword()
        
        result = combat.attack(attacker, defender, weapon)
        
        self.assertEqual(result["damage"], 40)
        self.assertEqual(defender.current_health, 60)


if __name__ == '__main__':
    unittest.main()