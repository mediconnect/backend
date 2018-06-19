from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework import routers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Hospital, HospitalReview
from .serializers import HospitalSerializer, HospitalReviewSerializer

from atlas.guarantor import use_serializer, any_exception_throws_400
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


class HospitalReviewViewSet(ModelViewSet):
    queryset = HospitalReview.objects.all()
    serializer_class = HospitalSerializer

    def get_permissions(self):
        """
            Permission class based on action type
        """
        if self.action == 'comment':
            # If not original file, only supervisor and translator can create
            permission_classes = [SupPermission]
            # TODO: This is not correct
        else:
            permission_classes = [SupPermission, IsAuthenticated]

        return [permission() for permission in permission_classes]

    def comment(self, request, **kwargs):

        if request.method == 'POST':

            # request.data is from the POST object. We want to take these
            # values and supplement it with the user.id that's defined
            # in our URL parameter
            data = {
                'comment': request.data['comment'],
                'score': request.data['score'],
                'customer': request.data['customer'],
            }

            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,)
            else:
                return Response(serializer.errors,)

        # Return GET by default
        else:
            serializer = self.serializer_class(instance=self.queryset, many=True)

            return Response(serializer.data)



router = routers.SimpleRouter()
router.register(r'hospital', HospitalViewSet)
urlpatterns = router.urls
