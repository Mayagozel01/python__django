from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=110, unique=True, blank=True)
	description = models.TextField(blank=True)

	class Meta:
		ordering = ["name"]

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name


class Size(models.Model):
	"""Represents a clothing size (S, M, L, XL, 38, 40, etc)."""
	name = models.CharField(max_length=30, unique=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name


class Color(models.Model):
	"""Represents a color option for a product."""
	name = models.CharField(max_length=30, unique=True)
	hex_code = models.CharField(max_length=7, blank=True, help_text="#RRGGBB optional")

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=270, unique=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	sizes = models.ManyToManyField(Size, blank=True, related_name="products")
	colors = models.ManyToManyField(Color, blank=True, related_name="products")
	stock = models.PositiveIntegerField(default=0)
	image = models.ImageField(upload_to="products/", blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at", "name"]

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.name} ({self.category})"

	def get_absolute_url(self):
		return reverse("shop:product_detail", args=[self.slug])

