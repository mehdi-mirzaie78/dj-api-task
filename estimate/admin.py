from django.contrib import admin
from .models import Estimate, EstimateEquipment


class EstimateEquipmentInline(admin.TabularInline):
    model = EstimateEquipment
    extra = 0


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    readonly_fields = ["created_on"]
    list_display = ["note", "id", "created_on", "created_by", "archive"]
    search_fields = ["note", "id", "created_by__email"]
    inlines = [EstimateEquipmentInline]


@admin.register(EstimateEquipment)
class EstimateEquipmentAdmin(admin.ModelAdmin):
    readonly_fields = ["created_on"]
    fields = ["estimate", "equipment", "quantity", "price_override"]
    list_display = ["estimate", "estimate__created_by", "equipment", "quantity", "price_override", "created_on"]
