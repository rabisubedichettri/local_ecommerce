import factory
from product.models import Category

class CategoryrFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category  # Connects to the Category model

    name = factory.Faker("word")  # Random category name
    description = factory.Faker("sentence")  # Random description
    meta_title = factory.Faker("sentence")  # Random meta title
    meta_description = factory.Faker("sentence")  # Random meta description
    is_active = factory.Faker("boolean")  # Random True/False value

