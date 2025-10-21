"""
Tests unitarios para el sistema de armadura.
Esta es la nueva funcionalidad agregada al laboratorio.
"""
import unittest
from src.armor_system import (
    LeatherArmor, PlateArmor, MagicShield, 
    EnchantedArmor, DummyArmor
)
from src.combat_system import Character, CombatSystem
from src.weapons import Sword
from src.damage_calculator import MockDamageCalculator


class TestLeatherArmor(unittest.TestCase):
    """Tests para armadura de cuero."""
    
    def test_leather_armor_creation(self):
        """Verifica la creación de armadura de cuero."""
        armor = LeatherArmor(defense=10)
        self.assertEqual(armor.get_defense(), 10)
        self.assertEqual(armor.get_name(), "Leather Armor")
    
    def test_leather_armor_absorbs_damage(self):
        """Verifica que la armadura absorbe 20% del daño."""
        armor = LeatherArmor()
        incoming_damage = 100
        final_damage = armor.absorb_damage(incoming_damage)
        
        # Debería absorber 20 de daño (20%)
        self.assertEqual(final_damage, 80)
    
    def test_leather_armor_durability_depletion(self):
        """Verifica explícitamente que la durabilidad se agota."""
        armor = LeatherArmor()
        
        # Usar la armadura exactamente 100 veces
        for _ in range(100):
            armor.absorb_damage(50)
        
        # La durabilidad debería ser 0
        self.assertEqual(armor._durability, 0)
        
        # El siguiente ataque no debería absorber daño
        final_damage = armor.absorb_damage(100)
        self.assertEqual(final_damage, 100)
    
    def test_leather_armor_minimum_damage(self):
        """Verifica que siempre se recibe al menos algo de daño."""
        armor = LeatherArmor()
        final_damage = armor.absorb_damage(10)
        self.assertGreater(final_damage, 0)


class TestPlateArmor(unittest.TestCase):
    """Tests para armadura de placas."""
    
    def test_plate_armor_creation(self):
        """Verifica la creación de armadura de placas."""
        armor = PlateArmor(defense=30)
        self.assertEqual(armor.get_defense(), 30)
        self.assertEqual(armor.get_name(), "Plate Armor")
    
    def test_plate_armor_high_absorption(self):
        """Verifica que la armadura de placas absorbe 50% del daño."""
        armor = PlateArmor()
        incoming_damage = 100
        final_damage = armor.absorb_damage(incoming_damage)
        
        # Debería absorber 50 de daño (50%)
        self.assertEqual(final_damage, 50)
    
    def test_plate_armor_durability_degrades_faster(self):
        """Verifica que la durabilidad se degrada más rápido."""
        armor = PlateArmor()
        
        # Usar la armadura 100 veces (debería gastar 200 de durabilidad)
        for _ in range(100):
            armor.absorb_damage(50)
        
        # La armadura debería estar sin durabilidad
        final_damage = armor.absorb_damage(100)
        self.assertEqual(final_damage, 100)
    
    def test_plate_armor_vs_leather_armor(self):
        """Compara la absorción entre armadura de placas y cuero."""
        plate = PlateArmor()
        leather = LeatherArmor()
        
        damage = 60
        
        plate_final = plate.absorb_damage(damage)
        leather_final = leather.absorb_damage(damage)
        
        # La armadura de placas debería absorber más
        self.assertLess(plate_final, leather_final)


class TestMagicShield(unittest.TestCase):
    """Tests para escudo mágico."""
    
    def test_magic_shield_creation(self):
        """Verifica la creación del escudo mágico."""
        shield = MagicShield(defense=20, mana=100)
        self.assertEqual(shield.get_defense(), 20)
        self.assertEqual(shield.get_name(), "Magic Shield")
        self.assertEqual(shield.get_mana(), 100)
    
    def test_magic_shield_absorption_with_full_mana(self):
        """Verifica absorción con maná completo."""
        shield = MagicShield(mana=100)
        incoming_damage = 100
        final_damage = shield.absorb_damage(incoming_damage)
        
        # Con maná completo, absorción es máxima (70%)
        self.assertLessEqual(final_damage, 30)
    
    def test_magic_shield_mana_consumption(self):
        """Verifica que el escudo consume maná al absorber daño."""
        shield = MagicShield(mana=100)
        initial_mana = shield.get_mana()
        
        shield.absorb_damage(60)
        
        # El maná debería haber disminuido
        self.assertLess(shield.get_mana(), initial_mana)
    
    def test_magic_shield_without_mana(self):
        """Verifica que sin maná no absorbe daño."""
        shield = MagicShield(mana=0)
        incoming_damage = 100
        final_damage = shield.absorb_damage(incoming_damage)
        
        # Sin maná, no debería absorber nada
        self.assertEqual(final_damage, 100)
    
    def test_magic_shield_recharge(self):
        """Verifica que el escudo puede recargarse."""
        shield = MagicShield(mana=100)
        
        # Gastar maná
        shield.absorb_damage(80)
        shield.absorb_damage(80)
        
        current_mana = shield.get_mana()
        
        # Recargar
        shield.recharge_mana(50)
        
        self.assertGreater(shield.get_mana(), current_mana)
    
    def test_magic_shield_recharge_cap(self):
        """Verifica que el maná no excede el máximo."""
        shield = MagicShield(mana=100)
        shield.absorb_damage(40)
        shield.recharge_mana(200)
        
        # No debería exceder 100
        self.assertEqual(shield.get_mana(), 100)
    
    def test_magic_shield_adaptive_absorption(self):
        """Verifica que la absorción se adapta al maná disponible."""
        shield = MagicShield(mana=100)
        
        damage = 100
        
        # Primera absorción con maná completo
        first_absorption = shield.absorb_damage(damage)
        
        # Reducir maná significativamente
        shield._mana = 20
        
        # Segunda absorción con poco maná
        second_absorption = shield.absorb_damage(damage)
        
        # Con menos maná, debería absorber menos
        self.assertGreater(second_absorption, first_absorption)


class TestEnchantedArmor(unittest.TestCase):
    """Tests para armadura encantada."""
    
    def test_enchanted_armor_creation(self):
        """Verifica la creación de armadura encantada."""
        armor = EnchantedArmor(defense=25)
        self.assertEqual(armor.get_defense(), 25)
        self.assertEqual(armor.get_name(), "Enchanted Armor")
    
    def test_enchanted_armor_absorbs_damage(self):
        """Verifica que la armadura absorbe daño."""
        armor = EnchantedArmor()
        incoming_damage = 100
        final_damage = armor.absorb_damage(incoming_damage)
        
        # Debería absorber al menos algo
        self.assertLess(final_damage, incoming_damage)
    
    def test_enchanted_armor_reflection_mechanic(self):
        """Verifica el mecanismo de reflexión."""
        armor = EnchantedArmor()
        
        # Realizar múltiples ataques
        reflection_count = 0
        total_attacks = 100
        
        for _ in range(total_attacks):
            armor.absorb_damage(50)
            if armor.did_reflect():
                reflection_count += 1
        
        # Debería haber reflejado aproximadamente 15% de los ataques
        # Permitimos un margen de error
        self.assertGreater(reflection_count, 5)
        self.assertLess(reflection_count, 30)
    
    def test_enchanted_armor_durability(self):
        """Verifica que la durabilidad disminuye."""
        armor = EnchantedArmor()
        
        for _ in range(150):
            armor.absorb_damage(50)
        
        # La armadura debería estar sin durabilidad
        final_damage = armor.absorb_damage(100)
        self.assertEqual(final_damage, 100)


class TestArmorIntegrationWithCombat(unittest.TestCase):
    """Tests de integración entre armadura y sistema de combate."""
    
    def test_character_with_different_armors(self):
        """Compara personajes con diferentes armaduras."""
        calculator = MockDamageCalculator(fixed_damage=100)
        combat = CombatSystem(calculator)
        
        attacker = Character("Knight", 100, 10)
        weapon = Sword(damage=50)
        
        # Defensor con armadura de cuero
        defender_leather = Character("Guard1", 100, 10, armor=LeatherArmor())
        result1 = combat.attack(attacker, defender_leather, weapon)
        
        # Defensor con armadura de placas
        defender_plate = Character("Guard2", 100, 10, armor=PlateArmor())
        result2 = combat.attack(attacker, defender_plate, weapon)
        
        # El defensor con armadura de placas debería recibir menos daño
        self.assertLess(result2["damage"], result1["damage"])
    
    def test_armor_protects_in_combat(self):
        """Verifica que la armadura protege en combate real."""
        calculator = MockDamageCalculator(fixed_damage=50)
        combat = CombatSystem(calculator)
        
        attacker = Character("Warrior", 100, 5)
        defender_no_armor = Character("Peasant", 100, 5)
        defender_with_armor = Character("Knight", 100, 5, armor=PlateArmor())
        weapon = Sword()
        
        # Ataque sin armadura
        result1 = combat.attack(attacker, defender_no_armor, weapon)
        
        # Ataque con armadura
        result2 = combat.attack(attacker, defender_with_armor, weapon)
        
        # La armadura debería reducir el daño significativamente
        self.assertLess(result2["damage"], result1["damage"])
        self.assertGreater(defender_with_armor.current_health, 
                          defender_no_armor.current_health)
    
    def test_equip_armor_mid_combat(self):
        """Verifica que se puede equipar armadura durante el combate."""
        calculator = MockDamageCalculator(fixed_damage=40)
        combat = CombatSystem(calculator)
        
        attacker = Character("Barbarian", 100, 8)
        defender = Character("Mage", 100, 8)
        weapon = Sword()
        
        # Primer ataque sin armadura
        result1 = combat.attack(attacker, defender, weapon)
        self.assertEqual(result1["damage"], 40)
        self.assertEqual(defender.current_health, 60)
        
        # Equipar armadura mágica
        defender.equip_armor(MagicShield(mana=100))
        
        # Segundo ataque con armadura
        result2 = combat.attack(attacker, defender, weapon)
        self.assertLess(result2["damage"], 40)
    
    def test_multiple_attacks_degrade_armor(self):
        """Verifica que múltiples ataques degradan la armadura."""
        calculator = MockDamageCalculator(fixed_damage=50)
        combat = CombatSystem(calculator)
        
        attacker = Character("Warrior", 200, 10)
        defender = Character("Knight", 10000, 10, armor=LeatherArmor())  # Aumentar vida
        weapon = Sword()
        
        damages = []
        
        # Realizar 105 ataques (la durabilidad es 100)
        for i in range(105):
            if not defender.is_alive():
                break
            result = combat.attack(attacker, defender, weapon)
            if result["success"]:
                damages.append(result["damage"])
        
        # Los últimos ataques deberían causar más daño
        # (cuando la armadura está sin durabilidad)
        # Comparamos los primeros 5 con los últimos 5
        self.assertGreater(sum(damages[-5:]) / 5, sum(damages[:5]) / 5)
    
    def test_magic_shield_runs_out_of_mana(self):
        """Verifica que el escudo mágico se queda sin maná."""
        calculator = MockDamageCalculator(fixed_damage=60)
        combat = CombatSystem(calculator)
        
        shield = MagicShield(mana=100)
        attacker = Character("Sorcerer", 100, 10)
        defender = Character("Paladin", 500, 10, armor=shield)
        weapon = Sword()
        
        initial_damages = []
        late_damages = []
        
        # Primeros 5 ataques
        for _ in range(5):
            result = combat.attack(attacker, defender, weapon)
            initial_damages.append(result["damage"])
        
        # Forzar bajo maná
        shield._mana = 10
        
        # Siguientes 5 ataques con poco maná
        for _ in range(5):
            result = combat.attack(attacker, defender, weapon)
            late_damages.append(result["damage"])
        
        # Con menos maná, debería absorber menos (más daño recibido)
        avg_initial = sum(initial_damages) / len(initial_damages)
        avg_late = sum(late_damages) / len(late_damages)
        
        self.assertGreater(avg_late, avg_initial)


class TestDummyArmor(unittest.TestCase):
    """Tests para armadura dummy (utilizada en testing)."""
    
    def test_dummy_armor_creation(self):
        """Verifica la creación de armadura dummy."""
        armor = DummyArmor(defense=5, absorption_rate=0.3)
        self.assertEqual(armor.get_defense(), 5)
        self.assertEqual(armor.get_name(), "Dummy Armor")
    
    def test_dummy_armor_consistent_absorption(self):
        """Verifica que la absorción es consistente."""
        armor = DummyArmor(absorption_rate=0.25)
        
        # Todos los ataques deberían absorber exactamente 25%
        for damage in [20, 40, 60, 80, 100]:
            expected = damage * 0.75
            actual = armor.absorb_damage(damage)
            self.assertEqual(actual, int(expected))
    
    def test_dummy_armor_tracks_calls(self):
        """Verifica que el dummy trackea las llamadas."""
        armor = DummyArmor()
        
        self.assertEqual(armor.damage_received_count, 0)
        
        armor.absorb_damage(50)
        self.assertEqual(armor.damage_received_count, 1)
        
        armor.absorb_damage(30)
        armor.absorb_damage(70)
        self.assertEqual(armor.damage_received_count, 3)


if __name__ == '__main__':
    unittest.main()