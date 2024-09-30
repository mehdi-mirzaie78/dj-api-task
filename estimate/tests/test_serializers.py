from django.test import TestCase
from rest_framework.test import APIRequestFactory
from estimate.serializers import EstimateSerializer
from estimate.models import Estimate, EstimateEquipment
from user.models import User
from management.models import Equipment


class EstimateSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )

        self.equipment1 = Equipment.objects.create(name="Equipment 1", price=100.00)
        self.equipment2 = Equipment.objects.create(name="Equipment 2", price=200.00)
        self.equipment3 = Equipment.objects.create(name="Equipment 3", price=300.00)

        self.context = {"request": self.factory.get("/")}
        self.context["request"].user = self.user

        self.estimate = Estimate.objects.create(
            note="Initial Estimate", created_by=self.user
        )
        EstimateEquipment.objects.create(
            estimate=self.estimate,
            equipment=self.equipment1,
            quantity=1,
            price_override=100.00,
        )
        EstimateEquipment.objects.create(
            estimate=self.estimate,
            equipment=self.equipment2,
            quantity=2,
            price_override=200.00,
        )

    def test_update_estimate_with_new_and_existing_equipments(self):
        estimate_data = {
            "note": "Updated Estimate",
            "equipments": [
                {
                    "id": self.estimate.estimateequipment_set.all()[0].id,
                    "equipment": self.equipment1.id,
                    "quantity": 10,
                    "price_override": 150,
                },
                {
                    "equipment": self.equipment3.id,
                    "quantity": 3,
                    "price_override": 250,
                },
            ],
        }

        serializer = EstimateSerializer(
            instance=self.estimate,
            data=estimate_data,
            partial=True,
            context=self.context,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated_estimate = serializer.save()

        updated_equipment = updated_estimate.estimateequipment_set.get(
            id=self.estimate.estimateequipment_set.all()[0].id
        )
        self.assertEqual(updated_equipment.quantity, 10)
        self.assertEqual(updated_equipment.price_override, 150.00)

        self.assertEqual(updated_estimate.estimateequipment_set.count(), 2)

        new_equipment = updated_estimate.estimateequipment_set.get(
            equipment=self.equipment3
        )
        self.assertEqual(new_equipment.quantity, 3)
        self.assertEqual(new_equipment.price_override, 250.00)

    def test_update_estimate_and_delete_not_updated_equipments(self):
        estimate_data = {
            "note": "Updated Estimate with deletions",
            "equipments": [
                {
                    "id": self.estimate.estimateequipment_set.all()[1].id,
                    "equipment": self.equipment2.id,
                    "quantity": 5,
                    "price_override": "250.00",
                },
            ],
        }

        serializer = EstimateSerializer(
            instance=self.estimate,
            data=estimate_data,
            partial=True,
            context=self.context,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated_estimate = serializer.save()

        self.assertEqual(updated_estimate.estimateequipment_set.count(), 1)

        remaining_equipment = updated_estimate.estimateequipment_set.get(
            equipment=self.equipment2
        )
        self.assertEqual(remaining_equipment.quantity, 5)
        self.assertEqual(remaining_equipment.price_override, 250.00)
