
from django.http import JsonResponse
from .tasks import my_task,make_pdf

def home(request):
    pdf_result=make_pdf.delay()
    addition_result = my_task.delay(10, 20)  # Runs asynchronously
    return JsonResponse({"pdf_result": pdf_result.id,
                        "addition_result":addition_result.id
                        })

def make_bill(request):
    pass



from api.v1.product.serializers import CategorySerializer,CategorySerializer_,SubCategorySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from django.shortcuts import get_object_or_404
from product.models import Category,SubCategory,Product,ProductImage,Price
from api.v1.responseFormat import responseFormat
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import ProductSerializer,ProductImageSerializer,PriceSerializer,ProductSpecificationSerializer
from .serializers import OfferDetailSerializer,OfferListSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import JSONParser
import json
from django.http import QueryDict


from .models import ProductSpecification,Offer

class CategoryList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        categories = Product.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return responseFormat(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return responseFormat(data=serializer.data, 
                        status=status.HTTP_201_CREATED,
                        message=f"{data.name} is added to Category List")

        return responseFormat(errors=serializer.errors, 
                             status=status.HTTP_400_BAD_REQUEST,
                             data=serializer.data,
                              message=f"solve the errors and resubmit")


class ProductList(APIView):
    parser_classes = (MultiPartParser, FormParser)  # File upload support

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return responseFormat(
            data=serializer.data,
            message="Product List Fetched Successfully.",
            status=status.HTTP_200_OK
        )

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)  # MultiPart data support
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
                message=f"{serializer.validated_data.get('name')} is added to Product List"
            )
        else:
            if 'featured_image' in request.data:
                del request.data['featured_image']  # Remove image if invalid
            return responseFormat(
                errors=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                data=request.data,
                message="Solve the errors and resubmit"
            )


class ProductDetail(APIView):
    
    parser_classes = (MultiPartParser, FormParser)  # File upload support

    def get(self, request,pk, format=None):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product)
        return responseFormat(
            data=serializer.data,
            message="Product List Fetched Successfully.",
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, format=None):
        """ Full update of a single product """
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Product updated successfully"
            )
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """ Partial update of a single product """
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Product partially updated successfully"
            )
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ Delete a single product """
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return responseFormat(status=status.HTTP_200_OK, message="Product deleted successfully")

class ProductImageListView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # File upload support

    def get(self, request, format=None):
        """ Retrieve all product images """
        product_images = ProductImage.objects.all()
        serializer = ProductImageSerializer(product_images, many=True)
        return Response(
            {"data": serializer.data, "message": "Product Images Fetched Successfully."},
            status=status.HTTP_200_OK
        )

    def post(self, request, format=None):
        """ Create a new product image """
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"data": serializer.data, "message": "Product Image Created Successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"errors": serializer.errors, "message": "Failed to create product image."},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductImageDetail(APIView):
    
    parser_classes = (MultiPartParser, FormParser)  # File upload support

    def get(self, request, pk, format=None):
        """ Retrieve a single product image """
        product_image = get_object_or_404(ProductImage, id=pk)
        serializer = ProductImageSerializer(product_image)
        return responseFormat(
            data=serializer.data,
            message="Product Image Fetched Successfully.",
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, format=None):
        """ Full update of a single product image """
        product_image = get_object_or_404(ProductImage, id=pk)
        serializer = ProductImageSerializer(product_image, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Product Image updated successfully"
            )
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """ Partial update of a single product image """
        product_image = get_object_or_404(ProductImage, id=pk)
        serializer = ProductImageSerializer(product_image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Product Image partially updated successfully"
            )
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ Delete a single product image """
        product_image = get_object_or_404(ProductImage, id=pk)
        product_image.delete()
        return responseFormat(status=status.HTTP_200_OK, message="Product Image deleted successfully")






    

    def get(self, request, pk, format=None):
        """ Retrieve a single product image """
        product_image = get_object_or_404(ProductImage, id=pk)
        serializer = ProductImageSerializer(product_image)
        return responseFormat(
            data=serializer.data,
            message="Product Image Fetched Successfully.",
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, format=None):
        """ Full update of a single product image """
        product_image = get_object_or_404(ProductImage, id=pk)
        serializer = ProductImageSerializer(product_image, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Product Image updated successfully"
            )
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """ Partial update of a single product image """
        product_image = get_object_or_404(ProductImage, id=pk)
        serializer = ProductImageSerializer(product_image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Product Image partially updated successfully"
            )
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ Delete a single product image """
        product_image = get_object_or_404(ProductImage, id=pk)
        product_image.delete()
        return responseFormat(status=status.HTTP_200_OK, message="Product Image deleted successfully")
    

class ProductPriceListView(APIView):

    def get(self, request, format=None):
        """ Retrieve all product images """
        product_prices = Price.objects.all()
        serializer = PriceSerializer(product_prices, many=True)
        return Response(
            {"data": serializer.data, "message": "Product Orginal Price Fetched Successfully."},
            status=status.HTTP_200_OK
        )

    def post(self, request, format=None):
        """ Create a new product image """
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"data": serializer.data, "message": "Product Orginal Created Successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"errors": serializer.errors, "message": "Failed to create product price."},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductImageDetail(APIView):
    
    parser_classes = (MultiPartParser, FormParser)  # File upload support

    def get(self, request, pk, format=None):
        """ Retrieve a single product image """
        product_image = get_object_or_404(ProductImage, id=pk)
        serializer = ProductImageSerializer(product_image)
        return responseFormat(
            data=serializer.data,
            message="Product Image Fetched Successfully.",
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, format=None):
        """ Full update of a single product image """
        product_image = get_object_or_404(ProductImage, id=pk)
        serializer = ProductImageSerializer(product_image, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Product Image updated successfully"
            )
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """ Partial update of a single product image """
        product_image = get_object_or_404(ProductImage, id=pk)
        serializer = ProductImageSerializer(product_image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Product Image partially updated successfully"
            )
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ Delete a single product image """
        product_image = get_object_or_404(ProductImage, id=pk)
        product_image.delete()
        return responseFormat(status=status.HTTP_200_OK, message="Product Image deleted successfully")



class ProductPriceDetail(APIView):

    def get(self, request, pk, format=None):
        product_price = get_object_or_404(Price, product_id=pk)
        serializer = PriceSerializer(product_price)
        return responseFormat(
            data=serializer.data,
            message="Product Price Fetched Successfully.",
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, format=None):
        product_price = get_object_or_404(Price, product_id=pk)
        serializer = PriceSerializer(product_price, data=request.data, partial=False, context={'product_id': pk})
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Product price updated successfully"
            )
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        product_price = get_object_or_404(Price, product_id=pk)
        serializer = PriceSerializer(product_price, data=request.data, partial=True, context={'product_id': pk})
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Product Price partially updated successfully"
            )
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product_price = get_object_or_404(Price, product_id=pk)
        product_price.delete()
        return responseFormat(status=status.HTTP_200_OK, message="Product price deleted successfully")


class ProductSpecificationView(APIView):

    def get(self, request, product_id, format=None):
        """ Retrieve all specifications of a product """
        product = get_object_or_404(Product, id=product_id)
        specifications = product.specifications.all()  # Get related specifications
        serializer = ProductSpecificationSerializer(specifications, many=True)
        return responseFormat(
            data=serializer.data,
            message="Product Specifications Fetched Successfully.",
            status=status.HTTP_200_OK
        )

    def post(self, request, product_id, format=None):
        """ Bulk insert product specifications """
        product = get_object_or_404(Product, id=product_id)

        # ✅ QueryDict लाई dictionary मा change गर्ने (Only if it's a QueryDict)
        if isinstance(request.data, QueryDict):
            data = json.loads(json.dumps(dict(request.data)))
            # Convert it to list of dictionaries
            formatted_data = [{"key": k, "value": v[0]} for k, v in data.items()]
        else:
            formatted_data = request.data  # If already JSON format
        
        serializer = ProductSpecificationSerializer(data=formatted_data, many=True)

        if serializer.is_valid():
            specifications = [
                ProductSpecification(product=product, **data) for data in serializer.validated_data
            ]
            ProductSpecification.objects.bulk_create(specifications)  # Bulk insert new specifications

            return responseFormat(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
                message="Product Specifications Added Successfully."
            )


class ProductSpecificationDetailView(APIView):

    def patch(self, request, spec_id, format=None):
        """ Partially update a single specification """
        specification = get_object_or_404(ProductSpecification, id=spec_id)
        serializer = ProductSpecificationSerializer(specification, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Product Specification Updated Successfully."
            )
        
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, spec_id, format=None):
        """ Delete a single specification """
        specification = get_object_or_404(ProductSpecification, id=spec_id)
        specification.delete()
        return responseFormat(status=status.HTTP_200_OK, message="Product Specification Deleted Successfully")


class OfferDetail(APIView):

    def get(self, request, pk, format=None):
        product_offer = get_object_or_404(Offer, product_id=pk)
        serializer = OfferDetailSerializer(product_offer)
        return responseFormat(
            data=serializer.data,
            message="Product Price Fetched Successfully.",
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, format=None):
        product_offer = get_object_or_404(Offer, product_id=pk)
        serializer = OfferDetailSerializer(product_offer, data=request.data, partial=False, context={'product_id': pk})
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Product price updated successfully"
            )
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        product_offer = get_object_or_404(Offer, product_id=pk)
        serializer = OfferDetailSerializer(product_offer, data=request.data, partial=True, context={'product_id': pk})
        if serializer.is_valid():
            serializer.save()
            return responseFormat(
                data=serializer.data,
                status=status.HTTP_200_OK,
                message="Product Price partially updated successfully"
            )
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product_offer = get_object_or_404(Offer, product_id=pk)
        product_offer.delete()
        return responseFormat(status=status.HTTP_200_OK, message="Product price deleted successfully")



class OfferListView(APIView):

    def get(self, request, format=None):
        """ Retrieve all product images """
        product_offers = Offer.objects.all()
        serializer = OfferListSerializer(product_offers, many=True)
        return Response(
            {"data": serializer.data, "message": "Product Orginal Price Fetched Successfully."},
            status=status.HTTP_200_OK
        )

    def post(self, request, format=None):
        """ Create a new product image """
        serializer = OfferListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"data": serializer.data, "message": "Product Orginal Created Successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"errors": serializer.errors, "message": "Failed to create product price."},
            status=status.HTTP_400_BAD_REQUEST
        )



from rest_framework.generics import RetrieveAPIView
from .serializers import FullProductSerializer
class ProductFullView(RetrieveAPIView):
    queryset = Product.objects.select_related('subcategory__category', 'price_details', 'offer_details').prefetch_related('product_images', 'specifications')
    serializer_class = FullProductSerializer