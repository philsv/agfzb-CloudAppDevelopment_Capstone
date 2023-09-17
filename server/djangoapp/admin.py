from django.contrib import admin

from .models import CarMake, CarModel


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5


class CarModelAdmin(admin.ModelAdmin):
    list_display = ["name", "dealer_id", "type", "year"]
    list_filter = ["dealer_id", "type", "year"]
    search_fields = ["name", "type"]


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ["name", "description"]
    list_filter = ["name"]
    search_fields = ["name"]


admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
