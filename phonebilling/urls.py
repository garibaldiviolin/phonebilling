from django.conf.urls import url, include
from rest_framework import routers
from serviceapi import views

router = routers.DefaultRouter()
router.register(r'startrecord', views.StartRecordViewSet)
router.register(r'endrecord', views.EndRecordViewSet)
router.register(r'phonebill', views.PhoneBillViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
