from datetime import datetime, timedelta
import uuid

from slot.models.timeslot import TimeSlot
from .serializers import SlotAdminSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import routers, filters


class SlotAdminViewSet(ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = SlotAdminSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    search_fields = ('@hospital__name', '@disease__name')
    ordering_fields = '__all__'

    def create(self, request, *args, **kwargs):
        pass  # not allowed


router = routers.DefaultRouter()
router.register('', SlotAdminViewSet)
urlpatterns = router.urls




