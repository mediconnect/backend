from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework import routers, filters
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from document.models import Document
from document.serializer import DocumentSerializer
import os.path

from atlas.permissions import SupPermission,TransPermission,ResPermission, IsOwner

import datetime


class FileUploadViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = (filters.OrderingFilter,filters.SearchFilter, DjangoFilterBackend,)
    filter_fields = ('res','owner','upload_at','type',)
    search_fields = ('=owner',)
    ordering_fields = '__all__'
    ordering = ('res','upload_at',)
    parser_classes = (FormParser, MultiPartParser)
    """
     def get_permissions(self):
        if self.action == 'list':
            permission_classes = [ResPermission]

        elif self.request.data.get('type') != 0 and self.action == 'create':
            # If not original file, only supervisor and translator can create
            permission_classes = [SupPermission, TransPermission]
user
        else:
            permission_classes = [SupPermission, IsOwnerOrReadOnly]

        return [permission() for permission in permission_classes]
    """
    # def get_queryset(self):
    #     """
    #     Filter/sort by query params in url
    #     """
    #     queryset = Document.objects.all()
    #     query_dic = {}
    #
    #     for field in Document._meta.get_fields():
    #         if field.name in self.request.query_params:
    #             query_dic[field.name] = self.request.query_params.get(field.name)
    #     queryset = queryset.filter(**query_dic)
    #     order_by = self.request.query_params.get('_order',None)
    #     if order_by:
    #         queryset.order_by(order_by)
    #     return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.id
        data['upload_at'] = datetime.datetime.now()
        data['extensions'] = os.path.splitext(request.data['file'].name)[1]
        serializer = DocumentSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':'Created','id':serializer.data['id']}, status=200)

        else:
            return Response(serializer.errors, status=400)


router = routers.DefaultRouter()
router.register(r'', FileUploadViewSet,base_name='document')
urlpatterns = router.urls
