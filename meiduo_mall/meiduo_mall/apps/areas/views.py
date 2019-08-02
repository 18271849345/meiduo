from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
# Create your views here.
from .models import Area
from .serializers import AreaSerializer,SubAreaSerializer
from rest_framework_extensions.cache.mixins import CacheResponseMixin


class AreasViewSet(CacheResponseMixin,ReadOnlyModelViewSet):
    pagination_class = None  # 区划信息不分页
    def get_queryset(self):
        if self.action=='list':
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()

    def get_serializer_class(self):
        if self.action=='list':
            return AreaSerializer
        else:
            return SubAreaSerializer
