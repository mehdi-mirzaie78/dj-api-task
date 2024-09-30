from django.test import TestCase
from management.models import Equipment
from user.models import User
from ..models import Estimate, EstimateEquipment, estimate_number_generator


class EstimateModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="testuser", password="testpassword")
        self.estimate = Estimate.objects.create(note="Test note", created_by=self.user)

    def test_estimate_creation(self):
        self.assertEqual(self.estimate.note, "Test note")
        self.assertEqual(self.estimate.created_by, self.user)
        self.assertIsNotNone(self.estimate.created_on)
        self.assertFalse(self.estimate.archive)

        self.assertEqual(Estimate.objects.count(), 1)

    def test_estimate_number_generator(self):

        estimate_long_id = str(self.estimate.created_by.id) + "100"
        estimate_date_created = str(self.estimate.created_on).replace("-", "")[2:8]
        expected_estimate_number = (
            estimate_date_created + estimate_long_id + str(self.estimate.id).zfill(3)
        )

        self.assertEqual(
            estimate_number_generator(self.estimate.id), expected_estimate_number
        )

    def test_estimate_str(self):
        expected_str = estimate_number_generator(self.estimate.id)
        self.assertEqual(str(self.estimate), expected_str)


class EstimateEquipmentModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="testuser", password="testpassword")
        self.estimate = Estimate.objects.create(note="Test note", created_by=self.user)
        self.equipment = Equipment.objects.create(name="Test Equipment", price=20)

    def test_estimate_equipment_creation(self):
        estimate_equipment = EstimateEquipment.objects.create(
            estimate=self.estimate,
            equipment=self.equipment,
            quantity=5,
            price_override=100,
        )

        self.assertEqual(estimate_equipment.estimate, self.estimate)
        self.assertEqual(estimate_equipment.equipment, self.equipment)
        self.assertEqual(estimate_equipment.quantity, 5)
        self.assertEqual(estimate_equipment.price_override, 100)
        self.assertIsNotNone(estimate_equipment.created_on)
        self.assertEqual(EstimateEquipment.objects.count(), 1)

    def test_estimate_number_generator(self):

        estimate_long_id = str(self.estimate.created_by.id) + "100"
        estimate_date_created = str(self.estimate.created_on).replace("-", "")[2:8]
        expected_estimate_number = (
            estimate_date_created + estimate_long_id + str(self.estimate.id).zfill(3)
        )

        self.assertEqual(
            estimate_number_generator(self.estimate.id), expected_estimate_number
        )

    def test_estimate_equipment_str(self):
        estimate_equipment = EstimateEquipment.objects.create(
            estimate=self.estimate,
            equipment=self.equipment,
            quantity=5,
            price_override=100,
        )

        expected_str = (
            estimate_number_generator(self.estimate.id) + " " + self.equipment.name
        )
        self.assertEqual(str(estimate_equipment), expected_str)
