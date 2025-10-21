"""
Tests unitarios para las armas del sistema.
"""
import unittest
from src.weapons import Sword, Bow, MagicStaff, DummyWeapon


class TestSword(unittest.TestCase):
    """Tests para la espada."""
    
    def test_sword_creation_default(self):
        """Verifica la creación de espada con valores por defecto."""
        sword = Sword()
        self.assertEqual(sword.get_damage(), 50)
        self.assertEqual(sword.get_name(), "Sword")
    
    def test_sword_creation_custom(self):
        """Verifica la creación de espada con daño personalizado."""
        sword = Sword(damage=75)
        self.assertEqual(sword.get_damage(), 75)


class TestBow(unittest.TestCase):
    """Tests para el arco."""
    
    def test_bow_creation_default(self):
        """Verifica la creación de arco con valores por defecto."""
        bow = Bow()
        self.assertEqual(bow.get_damage(), 40)
        self.assertEqual(bow.get_name(), "Bow")
    
    def test_bow_creation_custom(self):
        """Verifica la creación de arco con daño personalizado."""
        bow = Bow(damage=55)
        self.assertEqual(bow.get_damage(), 55)


class TestMagicStaff(unittest.TestCase):
    """Tests para el báculo mágico."""
    
    def test_magic_staff_creation_default(self):
        """Verifica la creación de báculo con valores por defecto."""
        staff = MagicStaff()
        self.assertEqual(staff.get_damage(), 70)  # 60 + 10 bonus
        self.assertEqual(staff.get_name(), "Magic Staff")
    
    def test_magic_staff_with_intelligence_bonus(self):
        """Verifica que el bonus de inteligencia se aplica."""
        staff = MagicStaff(damage=50, intelligence_bonus=20)
        self.assertEqual(staff.get_damage(), 70)
    
    def test_magic_staff_high_intelligence(self):
        """Verifica báculo con alta inteligencia."""
        staff = MagicStaff(damage=60, intelligence_bonus=30)
        self.assertEqual(staff.get_damage(), 90)


class TestDummyWeapon(unittest.TestCase):
    """Tests para el arma dummy."""
    
    def test_dummy_weapon_creation(self):
        """Verifica la creación de arma dummy."""
        weapon = DummyWeapon()
        self.assertEqual(weapon.get_damage(), 10)
        self.assertEqual(weapon.get_name(), "Dummy Weapon")
    
    def test_dummy_weapon_custom_damage(self):
        """Verifica arma dummy con daño personalizado."""
        weapon = DummyWeapon(damage=25)
        self.assertEqual(weapon.get_damage(), 25)


class TestWeaponComparison(unittest.TestCase):
    """Tests de comparación entre armas."""
    
    def test_weapon_damage_comparison(self):
        """Compara el daño de diferentes armas."""
        sword = Sword()
        bow = Bow()
        staff = MagicStaff()
        
        # El báculo debería hacer más daño que la espada
        self.assertGreater(staff.get_damage(), sword.get_damage())
        
        # La espada debería hacer más daño que el arco
        self.assertGreater(sword.get_damage(), bow.get_damage())
    
    def test_all_weapons_have_positive_damage(self):
        """Verifica que todas las armas tienen daño positivo."""
        weapons = [Sword(), Bow(), MagicStaff(), DummyWeapon()]
        
        for weapon in weapons:
            self.assertGreater(weapon.get_damage(), 0,
                             f"{weapon.get_name()} should have positive damage")


if __name__ == '__main__':
    unittest.main()