from .serializers import CategorySerializer,CategorySerializer_,SubCategorySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from django.shortcuts import get_object_or_404
from product.models import Category,SubCategory


from api.v1.responseFormat import responseFormat
class CategoryList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return responseFormat(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return responseFormat(data=serializer.data, 
                        status=status.HTTP_201_CREATED,
                        message=f"{data.name} is added to Category List")

        return responseFormat(errors=serializer.errors, 
                             status=status.HTTP_400_BAD_REQUEST,
                             data=serializer.data,
                              message=f"solve the errors and resubmit")

class CategoryDetail(APIView):
    """
    Retrieve, update or delete a single category instance.
    """
        
    def get(self, request, pk, format=None):
        """ Retrieve a single category """
        try:
            category = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return responseFormat(data={}, status=status.HTTP_404_NOT_FOUND, message=f"Category with ID {pk} not found.")
        
        serializer = CategorySerializer(category)
        return responseFormat(data=serializer.data, status=status.HTTP_200_OK, message="Category details fetched successfully")

    def put(self, request, pk, format=None):
        """ Full update of a single category """
        try:
            category = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return responseFormat(data={}, status=status.HTTP_404_NOT_FOUND, message=f"Category with ID {pk} does not exist.")
        
        serializer = CategorySerializer(category, data=request.data, partial=False)  # Full update
        if serializer.is_valid():
            serializer.save()
            return responseFormat(data=serializer.data, status=status.HTTP_200_OK, message="Category updated successfully")
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """ Partial update of a single category """
        try:
            category = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return responseFormat(data={}, status=status.HTTP_404_NOT_FOUND, message=f"Category with ID {pk} does not exist.")
        
        serializer = CategorySerializer(category, data=request.data, partial=True)  # Partial update
        if serializer.is_valid():
            serializer.save()
            return responseFormat(data=serializer.data, status=status.HTTP_200_OK, message="Category partially updated successfully")
        return responseFormat(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ Delete a single category """
        try:
            category = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return responseFormat(data={}, status=status.HTTP_404_NOT_FOUND, message=f"Category with ID {pk} does not exist.")
        
        category.delete()
        return responseFormat(status=status.HTTP_200_OK, message="Category deleted successfully")

class SubCategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.prefetch_related('subcategories')  # Optimized Query
        serializer = CategorySerializer_(categories, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self,request,format=None):
        pass

    def delete(self,request,format=None):
        pass

    
