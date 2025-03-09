from django.contrib.auth.models import User
from django.db import models

from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Name of the category
    description = models.TextField()  # Description of the category
    seo_slug = models.SlugField(unique=True,max_length=100)  # SEO-friendly slug
    meta_title = models.CharField(max_length=255)  # Meta title for SEO
    meta_description = models.TextField(max_length=200)  # Meta description for SEO
    is_active = models.BooleanField(default=False)  # Whether the category is active or not

    def save(self, *args, **kwargs):
        if not self.seo_slug:
            self.seo_slug = slugify(self.name)  # Generate slug from the category name if not provided
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")  # Link to the Category
    name = models.CharField(max_length=255)  # Name of the subcategory
    description = models.TextField(max_length=2000)  # Description of the subcategory
    seo_slug = models.SlugField(unique=True)  # SEO-friendly slug for subcategory
    meta_title = models.CharField(max_length=255, unique=True)  # Meta title for SEO
    meta_description = models.TextField(max_length=200)  # Meta description for SEO
    is_active = models.BooleanField(default=True)  # Whether the subcategory is active or not

    def save(self, *args, **kwargs):
        if not self.seo_slug:
            self.seo_slug = slugify(self.name)  # Generate slug from the subcategory name if not provided
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # subcategory
    slug = models.SlugField(unique=True)  # SEO-friendly URL
    featured_image = models.ImageField(upload_to='products/featured/')  # Can be null/optional
    alt_text = models.CharField(max_length=255)  # Alternative text for the image
    model_number = models.CharField(max_length=255, blank=True, null=True)  # Product model number
    subcategory=models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name="subcategories")
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Generate slug if not provided
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)  # This links the image to a product
    image = models.ImageField(upload_to='products/images/',blank=False)
    name = models.CharField(max_length=255)
    alt_text = models.CharField(max_length=255,)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.alt_text:
            self.alt_text = self.name
        super().save(*args, **kwargs)

class Price(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="price_details")
    original_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Price for {self.product.name}: {self.original_price}"

class Offer(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="offer_details")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Offer discount %
    is_active = models.BooleanField(default=False)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def get_offer_price(self):
        """Calculate the price after applying the offer (if active)."""
        if self.is_active and hasattr(self.product, 'price_details'):
            return self.product.price_details.original_price * (1 - self.discount_percentage / 100)
        return None  # No price available or inactive offer

    def __str__(self):
        return f"Offer for {self.product.name}: {self.discount_percentage}% OFF ({'Active' if self.is_active else 'Inactive'})"

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    key = models.CharField(max_length=255)  # Example: "Color", "RAM", "Storage"
    value = models.CharField(max_length=255)  # Example: "Red", "8GB", "256GB"

    def __str__(self):
        return f"{self.product.name} - {self.key}: {self.value}"


# class Review(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     rating = models.PositiveSmallIntegerField()  # 1-5 star rating
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["-created_at"]  # Latest reviews first

#     def __str__(self):
#         return f"Review by {self.user.username} on {self.product.name} - {self.rating}⭐"


# class Comment(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")  # Sub-comments
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["created_at"]  # Oldest first for natural conversation flow

#     def __str__(self):
#         return f"Comment by {self.user.username} on {self.product.name}"


