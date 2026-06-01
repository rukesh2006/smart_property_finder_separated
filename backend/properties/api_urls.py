from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AgentViewSet,
    CategoryViewSet,
    ContactMessageViewSet,
    PropertyImageViewSet,
    PropertyViewSet,
    WishlistViewSet,
    api_overview,
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='api-category')
router.register('agents', AgentViewSet, basename='api-agent')
router.register('properties', PropertyViewSet, basename='api-property')
router.register('property-images', PropertyImageViewSet, basename='api-property-image')
router.register('wishlist', WishlistViewSet, basename='api-wishlist')
router.register('contact-messages', ContactMessageViewSet, basename='api-contact-message')

urlpatterns = [
    path('', api_overview, name='api-overview'),
    path(
        'properties/<int:pk>/',
        PropertyViewSet.as_view({
            'get': 'retrieve',
            'post': 'partial_update',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='api-property-detail',
    ),
    path('', include(router.urls)),
]
