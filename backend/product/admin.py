from django.contrib import admin
from .models import Category, SubCategory,Product,ProductSpecification

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'seo_slug', 'meta_title', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'seo_slug': ('name',)}  # Automatically generate the slug from the category name
    fields = ('name', 'description', 'seo_slug', 'meta_title', 'meta_description', 'is_active')
    list_filter = ('is_active',)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'seo_slug', 'meta_title', 'is_active')
    search_fields = ('name', 'category__name')
    prepopulated_fields = {'seo_slug': ('name',)}  # Automatically generate the slug from the subcategory name
    fields = ('name', 'category', 'description', 'seo_slug', 'meta_title', 'meta_description', 'is_active')
    list_filter = ('is_active', 'category')

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product)
admin.site.register(ProductSpecification)
