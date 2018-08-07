from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework import routers
from rest_framework.response import Response
from rest_framework.decorators import (api_view, permission_classes, action)

from django.http import JsonResponse,Http404

from document.models import Document
from document.serializer import DocumentSerializer

from atlas.guarantor import use_serializer, any_exception_throws_400
from atlas.locator import AModule
from atlas.permissions import SupPermission,TransPermission,ResPermission, IsOwnerOrReadOnly

import datetime

class FileUploadViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser,)
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

    def create(self, request, *args, **kwargs):
        serializer = DocumentSerializer(data = request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(owner=self.request.user,
                        data=self.request.data.get('data'),
                        type = self.request.data.get('type'),
                        upload_at = datetime.datetime.now(),
                        resid = self.request.data.get('resid'))

        return Response({'id': serializer.id}, status=201)


router = routers.SimpleRouter()

router.register(r'document', FileUploadViewSet)
urlpatterns = router.urls