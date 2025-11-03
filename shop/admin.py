from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "slug")
	prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
	list_display = ("name",)


@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
	list_display = ("name", "hex_code")


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "category", "price", "stock", "created_at")
	list_filter = ("category", "sizes", "colors")
	search_fields = ("name", "description")
	prepopulated_fields = {"slug": ("name",)}
