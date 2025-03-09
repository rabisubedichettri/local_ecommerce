from .models import Category,SubCategory,Product,ProductSpecification
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ProductImage,Product,Price,Offer
from django.shortcuts import get_object_or_404


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
        

class ProductSerializer(serializers.ModelSerializer):
    featured_image = serializers.ImageField(required=True)  # 🔥 File upload field added

    class Meta:
        model = Product
        fields = '__all__'



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'  # OR specify the required fields

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        exclude = ['product']  # Exclude product field from form fields

    def create(self, validated_data):
        product_id = self.context['product_id']  # Get product_id from context
        validated_data['product'] = get_object_or_404(Product, id=product_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        product_id = self.context['product_id']
        validated_data['product'] = get_object_or_404(Product, id=product_id)
        return super().update(instance, validated_data)




class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = [ 'key', 'value']



class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        exclude = ['product']  # Exclude product field from form fields

    def create(self, validated_data):
        product_id = self.context['product_id']  # Get product_id from context
        validated_data['product'] = get_object_or_404(Product, id=product_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        product_id = self.context['product_id']
        validated_data['product'] = get_object_or_404(Product, id=product_id)
        return super().update(instance, validated_data)



class OfferListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields='__all__'
  


class FullProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.CharField(source='subcategory.name')
    category = serializers.CharField(source='subcategory.category.name')
    price = serializers.DecimalField(source='price.original_price', max_digits=10, decimal_places=2, required=False)
    offer = serializers.DecimalField(source='offer.discount_percentage', max_digits=5, decimal_places=2, required=False)
    offer_price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'subcategory','model_number','price','specifications','offer','offer_price','description','images']

    def get_offer_price(self, obj):
        return obj.offer.get_offer_price() if hasattr(obj, 'offer') and obj.offer.is_active else None

    def get_images(self, obj):
        return [{"url": img.image.url, "alt_text": img.alt_text} for img in obj.product_images.all()]

    def get_specifications(self, obj):
        return [{"key": spec.key, "value": spec.value} for spec in obj.specifications.all()]
