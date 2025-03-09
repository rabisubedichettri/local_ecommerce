from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from django.contrib import admin

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

def trigger_error(request):
    division_by_zero = 1 / 0



urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('sentry-debug/', trigger_error),
]

urlpatterns += [
    path('authtication/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('authtication/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('authtication/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += [    
    path("api/", include("api.urls", namespace="api")),
    path("admin/", admin.site.urls),
]





class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication

    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}!"})

urlpatterns += [
    path('api/protected/', ProtectedView.as_view(), name='protected-view'),
]


from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns +=[
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   
]