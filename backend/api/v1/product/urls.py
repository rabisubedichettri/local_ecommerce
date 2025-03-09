from django.urls import path, include
from .views import CategoryList,CategoryDetail,SubCategoryList


from product.views import ProductDetail,ProductList,ProductImageDetail,ProductImageListView,ProductPriceListView,ProductPriceDetail
from product.views import ProductSpecificationView,ProductSpecificationDetailView,OfferListView,OfferDetail,ProductFullView
app_name="product"
urlpatterns = [
    path("category/",CategoryList.as_view(),name="category_list"),
    path("category/<int:pk>/",CategoryDetail.as_view(),name="category_list"),
    path("category/subcategory/",SubCategoryList.as_view(),name="ZZ"),
    path("detail/<int:pk>/",ProductDetail.as_view(),name="detail"),
    path("list/",ProductList.as_view(),name="list"),
    path('product-image/<int:pk>/', ProductImageDetail.as_view(), name='product-image-detail'),
    path('product-image-list/',ProductImageListView.as_view(),name="product-image-list"),
    path('product-price-list/',ProductPriceListView.as_view(),name="prodct-price-list"),
    path('product-price-detail/<int:pk>/',ProductPriceDetail.as_view(),name="product-price-detail"),
    path('product/<int:product_id>/specifications/', ProductSpecificationView.as_view(), name="product-specifications"),
    path('product/specification/<int:spec_id>/', ProductSpecificationDetailView.as_view(), name="product-specification-detail"),
    
    path('product-offer-list/',OfferListView.as_view(),name="prodct-offer-list"),
    path('product-offer-detail/<int:pk>/',OfferDetail.as_view(),name="product-offer-detail"),
    path('products/<int:pk>/',ProductFullView.as_view(),name="product_full_view"),
 

]