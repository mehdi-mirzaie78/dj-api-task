from rest_framework import serializers
from django.db import transaction
from .models import Estimate, EstimateEquipment


class EstimateEquipmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = EstimateEquipment
        fields = ['id', 'equipment', 'quantity', 'price_override', 'created_on']
        read_only_fields = ["created_on"]


class EstimateSerializer(serializers.ModelSerializer):
    equipments = EstimateEquipmentSerializer(write_only=True, many=True, required=False)
    equipments_list = EstimateEquipmentSerializer(source='estimateequipment_set', read_only=True, many=True)
    archive = serializers.BooleanField(required=False)

    class Meta:
        model = Estimate
        fields = ['id', 'note', 'archive', 'equipments', 'equipments_list']

    def create(self, validated_data):
        user = self.context['request'].user
        equipments_data = validated_data.pop('equipments', [])
        with transaction.atomic():
            estimate = Estimate.objects.create(created_by=user, **validated_data)

            equipment_instances = [
                EstimateEquipment(estimate=estimate, **equipment_data) for equipment_data in equipments_data
            ]
            EstimateEquipment.objects.bulk_create(equipment_instances)
            return estimate

    # This approach is fine too but in small datasets
    # def update(self, instance, validated_data):
    #     equipments_data = validated_data.pop('equipments', [])
    #
    #     # Update the Estimate object
    #     instance.note = validated_data.get('note', instance.note)
    #     instance.archive = validated_data.get('archive', instance.archive)
    #     instance.save()
    #
    #     instance.estimateequipment_set.all().delete()
    #     for equipment_data in equipments_data:
    #         EstimateEquipment.objects.create(estimate=instance, **equipment_data)
    #
    #     return instance

    # I use this approach because of the performance if we have large number of records
    # we can update the existing records and add new records or delete the records that we don't need
    # This solution is more complex it has higher performance
    def update(self, instance, validated_data):
        self.equipments_data = validated_data.pop('equipments', [])
        with transaction.atomic():
            instance.note = validated_data.get('note', instance.note)
            instance.archive = validated_data.get('archive', instance.archive)
            instance.save()

            self.current_equipments = list(instance.estimateequipment_set.all())

            # Update existing items and create new ones
            self.existing_equipments_map = {item.id: item for item in self.current_equipments}
            self.updated_ids = set()

            self._update_existing_items_or_create_new_items(instance)
            self._delete_not_updated_items()

            return instance

    def _update_existing_items_or_create_new_items(self, instance):
        for equipment_data in self.equipments_data:
            equipment_id = equipment_data.get('id')

            if equipment_id and equipment_id in self.existing_equipments_map:
                # Update existing equipment item
                equipment_instance = self.existing_equipments_map[equipment_id]
                equipment_instance.equipment = equipment_data['equipment']
                equipment_instance.quantity = equipment_data['quantity']
                equipment_instance.price_override = equipment_data.get('price_override',
                                                                       equipment_instance.price_override)
                equipment_instance.save()
                self.updated_ids.add(equipment_id)
            else:
                # Create new equipment item
                EstimateEquipment.objects.create(estimate=instance, **equipment_data)

    def _delete_not_updated_items(self):
        # Delete any items that weren't updated
        for equipment_instance in self.current_equipments:
            if equipment_instance.id not in self.updated_ids:
                equipment_instance.delete()
