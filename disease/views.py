from rest_framework.viewsets import ModelViewSet
from rest_framework import routers
from django.http.request import QueryDict

from .models import Disease
from .serializers import DiseaseSerializer

from atlas.permissions import SupPermission, TransPermission, ResPermission, IsOwnerOrReadOnly


class DiseaseViewSet(ModelViewSet):
    serializer_class = DiseaseSerializer

    def get_permissions(self):
        if self.action == 'create':
            # If not original file, only supervisor and translator can create
            permission_classes = [SupPermission]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def get_queryset(self):

        if self.action == 'list':

            queryset = Disease.objects.all()

            query = QueryDict(self.request.query_params.get('query')).dict()

            return queryset.filter(**query)

        return Disease.objects.all()



router = routers.SimpleRouter()

router.register(r'disease', DiseaseViewSet,base_name='disease')
urlpatterns = router.urls
