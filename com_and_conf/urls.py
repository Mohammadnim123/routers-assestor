from rest_framework.routers import DefaultRouter
from .views import PublicMapperAPIView


api_router = DefaultRouter()
api_router.register('', PublicMapperAPIView, basename='')
urlpatterns = api_router.urls