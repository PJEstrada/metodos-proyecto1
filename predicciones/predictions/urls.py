from django.conf.urls import url, include
from rest_framework import routers
from predictions.views import  UploadDataSetViewSet

router = routers.DefaultRouter()
router.register('dataset', UploadDataSetViewSet, 'dataset')

urlpatterns = [
    url(r'^', include(router.urls))
]