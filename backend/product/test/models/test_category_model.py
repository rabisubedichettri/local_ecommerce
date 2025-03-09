from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from product.models import Category
from django.utils.text import slugify

class CategoryModelTest(TestCase):
    """ ✅ Test cases for the Category model """

    def test_create_category(self):
        """ ✅ Test successful category creation with valid data """
        category = Category.objects.create(
            name="Electronics",
            description="All electronic gadgets and devices",
            meta_title="Best Electronics Online",
            meta_description="Find all electronic gadgets and devices here.",
            is_active=True
        )

        # ✅ Validate stored values
        self.assertEqual(category.name, "Electronics")
        self.assertEqual(category.description, "All electronic gadgets and devices")
        self.assertEqual(category.meta_title, "Best Electronics Online")
        self.assertEqual(category.meta_description, "Find all electronic gadgets and devices here.")
        self.assertEqual(category.seo_slug, slugify("Electronics"))  # Slug should be auto-generated
        self.assertTrue(category.is_active)

        # ✅ Validate Data Types
        self.assertIsInstance(category.name, str)
        self.assertIsInstance(category.description, str)
        self.assertIsInstance(category.meta_title, str)
        self.assertIsInstance(category.meta_description, str)
        self.assertIsInstance(category.seo_slug, str)
        self.assertIsInstance(category.is_active, bool)

    def test_unique_name_constraint(self):
        """ ❌ Test that category name must be unique """
        Category.objects.create(
            name="Electronics",
            description="All electronic gadgets and devices",
            meta_title="Best Electronics Online",
            meta_description="Find all electronic gadgets and devices here."
        )
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name="Electronics",  # Same name should cause IntegrityError
                description="Duplicate category",
                meta_title="Duplicate",
                meta_description="Duplicate entry."
            )

    def test_seo_slug_auto_generation(self):
        """ ✅ Test that seo_slug is auto-generated when not provided """
        category = Category.objects.create(
            name="New Category",
            description="Test description",
            meta_title="SEO Test",
            meta_description="SEO Test Meta"
        )
        self.assertEqual(category.seo_slug, slugify("New Category"))

    def test_is_active_field(self):
        """ ✅ Test the 'is_active' field with various cases """

        # Test case 1: `is_active` not provided, should default to False
        category1 = Category.objects.create(
            name="Inactive Category",
            description="Category without active status",
            meta_title="Meta Title",
            meta_description="Meta Description"
        )
        self.assertFalse(category1.is_active)  # Default should be False

        # Test case 2: `is_active` set to True
        category2 = Category.objects.create(
            name="Active Category",
            description="Category with active status",
            meta_title="Meta Title",
            meta_description="Meta Description",
            is_active=True  # Explicitly setting is_active to True
        )
        self.assertTrue(category2.is_active)  # Should be True as set

        # Test case 3: `is_active` set to False explicitly
        category3 = Category.objects.create(
            name="Deactivated Category",
            description="Category with inactive status",
            meta_title="Meta Title",
            meta_description="Meta Description",
            is_active=False  # Explicitly setting is_active to False
        )
        self.assertFalse(category3.is_active)  # Should be False as set

    def test_max_length_constraints(self):
        """ ❌ Test max_length constraints on fields """

        # Test for `name` field exceeding max_length
        category1 = Category(
            name="A" * 300,  # Exceeding `name` max_length (255)
            description="Test description",
            meta_title="Meta",
            meta_description="Meta Description"
        )
        with self.assertRaises(ValidationError):
            category1.full_clean()  # Validate before saving

        # Test for `description` field exceeding max_length
        category2 = Category(
            name="Valid Name",
            description="A" * 1001,  # Exceeding `description` max_length (1000)
            meta_title="Meta Title",
            meta_description="Meta Description"
        )
        with self.assertRaises(ValidationError):
            category2.full_clean()  # Validate before saving

        # Test for `meta_title` field exceeding max_length
        category3 = Category(
            name="Valid Name",
            description="Test description",
            meta_title="A" * 256,  # Exceeding `meta_title` max_length (255)
            meta_description="Meta Description"
        )
        with self.assertRaises(ValidationError):
            category3.full_clean()  # Validate before saving

        # Test for `meta_description` field exceeding max_length
        category4 = Category(
            name="Valid Name",
            description="Test description",
            meta_title="Meta Title",
            meta_description="A" * 201  # Exceeding `meta_description` max_length (200)
        )
        with self.assertRaises(ValidationError):
            category4.full_clean()  # Validate before saving
    
    def test_missing_required_fields(self):
        """ ❌ Test that missing required fields raise ValidationError """
        
        # Missing `name`
        category1 = Category(
            description="Test description",
            meta_title="Meta Title",
            meta_description="Meta Description"
        )
        with self.assertRaises(ValidationError):
            category1.full_clean()

        # Missing `description`
        category2 = Category(
            name="No Description",
            meta_title="Meta Title",
            meta_description="Meta Description"
        )
        with self.assertRaises(ValidationError):
            category2.full_clean()

        # Missing `meta_title`
        category3 = Category(
            name="No Meta Title",
            description="Test description",
            meta_description="Meta Description"
        )
        with self.assertRaises(ValidationError):
            category3.full_clean()

        # Missing `meta_description`
        category4 = Category(
            name="No Meta Description",
            description="Test description",
            meta_title="Meta Title"
        )
        with self.assertRaises(ValidationError):
            category4.full_clean()

from product.test.factories import CategoryrFactory

class CategorydModelTest(TestCase):
    def test_category_creation(self):
        """ ✅ Test category creation dynamically using factory """
        category = CategoryrFactory()

        self.assertIsInstance(category, Category)  # Object should be a Category instance
        self.assertTrue(len(category.name) > 0)  # Name should not be empty
        self.assertTrue(len(category.description) > 0)  # Description should not be empty

    def test_category_data(self):
        """ ✅ Check what data the factory generates """
        category = CategoryrFactory()
        print(f"Name: {category.name}")
        print(f"Description: {category.description}")
        print(f"Meta Title: {category.meta_title}")
        print(f"Meta Description: {category.meta_description}")
        print(f"Is Active: {category.is_active}")