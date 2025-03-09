from product.models import Category,SubCategory
from rest_framework import serializers
from django.contrib.auth import get_user_model

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields=[ 'id',"name",
        "description",
        "seo_slug",
        "meta_title",
        "meta_description",
        ]



class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"

class CategorySerializer_(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"