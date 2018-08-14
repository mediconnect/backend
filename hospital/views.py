from django.http.request import QueryDict
from rest_framework.viewsets import ModelViewSet
from rest_framework import routers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Hospital, HospitalReview,LikeHospital
from .serializers import HospitalSerializer, HospitalReviewSerializer,LikeHospitalSerializer

from atlas.permissions import SupPermission, CanReviewPermission


class HospitalViewSet(ModelViewSet):

    serializer_class = HospitalSerializer
    """
    def get_permissions(self):
        if self.action == 'create':
            # If not original file, only supervisor and translator can create
            # permission_classes = [SupPermission]
            permission_classes=[]
        else:
            permission_classes = [SupPermission, IsAuthenticated]
    
        return [permission() for permission in permission_classes]
    """
    def get_queryset(self):

        if self.action == 'list':

            queryset = Hospital.objects.all()

            query = QueryDict(self.request.query_params.get('query')).dict()

            return queryset.filter(**query)

        return Hospital.objects.all()



class HospitalReviewViewSet(ModelViewSet):
    queryset = HospitalReview.objects.all()
    serializer_class = HospitalReviewSerializer

    def get_permissions(self):
        """
            Permission class based on action type
        """
        if self.action == 'comment':
            permission_classes = [CanReviewPermission]
            # TODO: This is not correct
        else:
            permission_classes = [SupPermission]

        return [permission() for permission in permission_classes]

    def comment(self, payload, request, **kwargs):

        if request.method == 'POST':
            serializer = self.serializer_class(**payload)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,)
            else:
                return Response(serializer.errors,)

        # Return GET by default
        else:
            serializer = self.serializer_class(instance=self.queryset, many=True)

            return Response(serializer.data)


class LikeHospitalReviewViewSet(ModelViewSet):
    queryset = LikeHospital.objects.all()
    serializer_class = LikeHospitalSerializer

    def get_permissions(self):
        return [IsAuthenticated,]

    def mark(self, payload, request, **kwargs):

        if request.method == 'POST':
            serializer = self.serializer_class(**payload)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, )
            else:
                return Response(serializer.errors, )

        # Return GET by default
        else:
            serializer = self.serializer_class(instance=self.queryset, many=True)

            return Response(serializer.data)


router = routers.SimpleRouter()
router.register(r'hospital', HospitalViewSet,base_name='hospital')
urlpatterns = router.urls
