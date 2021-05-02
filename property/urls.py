from django.urls import path, include

from rest_framework.routers import DefaultRouter

from property import views

router = DefaultRouter()
router.register('imobiliarias', views.RealEstateViewSet)
router.register('imoveis', views.PropertyViewSet)

app_name = 'property'

urlpatterns = [
    path('', include(router.urls))
]
