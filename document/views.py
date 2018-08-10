from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.viewsets import ModelViewSet
from rest_framework import routers
from rest_framework.response import Response


from document.models import Document
from document.serializer import DocumentSerializer
import uuid
import os.path


from atlas.permissions import SupPermission,TransPermission,ResPermission, IsOwnerOrReadOnly

import datetime


class FileUploadViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

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


    def create(self, request, *args, **kwargs):

        mutable = request.POST._mutable
        request.POST._mutable = True

        request.data.update({'id' : uuid.uuid4(),
                             'owner':request.user.id,
                             'upload_at':datetime.datetime.now(),
                             'extensions':os.path.splitext(request.data['file'].name)[1]})

        request.POST._mutable = mutable

        serializer = DocumentSerializer(data=request.data,)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            print(serializer.data)


            return Response({'msg':'Created','id':serializer.data['id']}, status=201)

        else:
            return Response(serializer.errors, status=400)

router = routers.SimpleRouter()
router.register(r'document/', FileUploadViewSet)
urlpatterns = router.urls
