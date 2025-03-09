from django.urls import path, include

app_name = "v1"
urlpatterns = [
    
    path("product/",include("api.v1.product.urls",namespace='product')),
]