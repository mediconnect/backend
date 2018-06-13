from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework import routers
from rest_framework.permissions import IsAuthenticated

from .models import Hospital
from .serializers import HospitalSerializer

from atlas.guarantor import use_serializer, any_exception_throws_400
from atlas.locator import AModule
from atlas.permissions import SupPermission,TransPermission,ResPermission, IsOwnerOrReadOnly

class HospitalViewSet(ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def get_permissions(self):
        """
            Permission class based on action type
        """
        if self.action == 'create':
            # If not original file, only supervisor and translator can create
            permission_classes = [SupPermission]
        else:
            permission_classes = [SupPermission, IsAuthenticated]

        return [permission() for permission in permission_classes]


router = routers.SimpleRouter()
router.register(r'hospital', HospitalViewSet)
urlpatterns = router.urls
