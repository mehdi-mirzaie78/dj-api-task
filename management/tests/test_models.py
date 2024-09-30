from django.test import TestCase
from ..models import Equipment


class EquipmentModelTest(TestCase):

    def setUp(self):
        self.equipment = Equipment.objects.create(name="Excavator", price=15000.00)

    def test_create_equipment(self):
        self.assertEqual(self.equipment.name, "Excavator")
        self.assertEqual(self.equipment.price, 15000.00)
        self.assertTrue(self.equipment.flag)
        self.assertIsNotNone(self.equipment.created_at)
        self.assertIsNotNone(self.equipment.updated_at)

    def test_string_representation(self):
        self.assertEqual(str(self.equipment), "Excavator")

    def test_delete_equipment(self):
        equipment_to_delete = Equipment.objects.create(name="To Delete", price=5000)
        equipment_to_delete_id = equipment_to_delete.id
        equipment_to_delete.delete()

        with self.assertRaises(Equipment.DoesNotExist):
            Equipment.objects.get(id=equipment_to_delete_id)
