from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.views import APIView
from rest_framework import routers
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import (api_view, permission_classes, action)

from django.http import JsonResponse,Http404

from document.models import Document
from document.serializer import DocumentSerializer
import uuid

from atlas.permissions import SupPermission,TransPermission,ResPermission, IsOwnerOrReadOnly

import datetime

class FileUploadView(APIView):

    parser_classes = (FormParser,MultiPartParser)
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

    def post(self, request,*args, **kwargs):
        mutable = request.POST._mutable
        request.POST._mutable = True

        request.data.update({'id' : uuid.uuid4(),
                             'owner':request.user.id,
                             'upload_at':datetime.datetime.now()})
        print(request.data)
        request.POST._mutable = mutable

        serializer = DocumentSerializer(data=request.data,)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':'Created','id':serializer.data['id']}, status=201)
        else:
            return Response(serializer.errors, status=400)


from django.urls import path

urlpatterns = [
    path('^document/upload/', FileUploadView.as_view(), name='document-upload'),
]
