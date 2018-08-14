from rest_framework.viewsets import ModelViewSet
from rest_framework import routers
from rest_framework.permissions import IsAuthenticated

from .models import Disease
from .serializers import DiseaseSerializer

from atlas.permissions import SupPermission, TransPermission, ResPermission, IsOwnerOrReadOnly


class DiseaseViewSet(ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    """
    def get_permissions(self):
    
        if self.action == 'create':
            # If not original file, only supervisor and translator can create
            permission_classes = []
        else:
            permission_classes = [SupPermission, IsAuthenticated]
    
        return [permission() for permission in permission_classes]
    """



router = routers.SimpleRouter()
router.register(r'disease', DiseaseViewSet)
urlpatterns = router.urls
