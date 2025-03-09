from django.test import TestCase
from product.models import Category, SubCategory

class CategoryModelTestCase(TestCase):
    def setUp(self):
        """Setup test data before each test case."""
        self.category = Category.objects.create(name="Electronics")

    def test_category_creation(self):
        """Test if category is created correctly."""
        self.assertEqual(self.category.name, "Electronics")

class SubCategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.subcategory = SubCategory.objects.create(name="Laptops", parent_category=self.category)

    def test_subcategory_creation(self):
        """Test if subcategory is created under category correctly."""
        self.assertEqual(self.subcategory.name, "Laptops")
        self.assertEqual(self.subcategory.parent_category, self.category)
