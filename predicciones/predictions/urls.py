from django.conf.urls import url, include
from rest_framework import routers
from predictions.views import  UploadDataSetViewSet
import predictions.views as views
router = routers.DefaultRouter()
router.register('dataset', UploadDataSetViewSet, 'dataset')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(
        r'^meditions/$',
        views.getDataSet,
        name='get_data_set'
    ),
]