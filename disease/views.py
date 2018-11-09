from rest_framework.viewsets import ModelViewSet
from rest_framework import routers, filters

from django.http.request import QueryDict
from django_filters.rest_framework import DjangoFilterBackend

from .models import Disease
from .serializers import DiseaseSerializer

from atlas.permissions import SupPermission, TransPermission, ResPermission, IsOwnerOrReadOnly


class DiseaseViewSet(ModelViewSet):
    serializer_class = DiseaseSerializer
    queryset = Disease.objects.all()
    filter_backends = (filters.SearchFilter,DjangoFilterBackend,)
    filter_fields = ('name','keyword','category')
    search_fields = ('=name','=keyword')
    # def get_permissions(self):
    #     if self.action == 'create':
    #         # If not original file, only supervisor and translator can create
    #         permission_classes = [SupPermission]
    #     else:
    #         permission_classes = []
    #
    #     return [permission() for permission in permission_classes]

    # def get_queryset(self):
    #     """
    #     Filter/sort by query param in url
    #     """
    #     queryset = Disease.objects.all()
    #     query_dic = {}
    #
    #     for field in Disease._meta.get_fields():
    #         if field.name in self.request.query_params:
    #             query_dic[field.name] = self.request.query_params.get(field.name)
    #     queryset = queryset.filter(**query_dic)
    #     order_by = self.request.query_params.get('_order',None)
    #     if order_by:
    #         queryset.order_by(order_by)
    #     return queryset


router = routers.DefaultRouter()

router.register(r'', DiseaseViewSet,base_name='disease')
urlpatterns = router.urls
