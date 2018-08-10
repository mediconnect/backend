from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from atlas.creator import assert_or_throw
from atlas.guarantor import use_serializer, any_exception_throws_400
from atlas.locator import AModule

from .serializer import FileTypeSerializer, RequirementSerializer
from .models import FileType, Requirement

requirement_module = AModule()


@requirement_module.route("ftype/create", name="filetype_create")
class FileTypeCreate(APIView):

    @any_exception_throws_400
    @use_serializer(Serializer=FileTypeSerializer, pass_in='data')
    def post(self, payload, format=None):
        new_type = FileType.objects.create(name=payload['name'], description=payload['description'])
        return JsonResponse(FileTypeSerializer(new_type).data)


@requirement_module.route("ftype/(?<ftid>.+?)/get", name="filetype_get")
class FileTypeGet(APIView):

    @any_exception_throws_400
    def get(self, request, ftid, format=None):
        ftype = FileType.objects.get(id=ftid)
        return JsonResponse(FileTypeSerializer(ftype).data)


@requirement_module.route("ftype/(?<ftid>.+?)/retire", name="filetype_retire")
class FileTypeRetire(APIView):

    @any_exception_throws_400
    def post(self, request, ftid, format=None):
        ftype = FileType.objects.get(id=ftid)
        ftype.obsolete = True
        ftype.save()
        return JsonResponse(FileTypeSerializer(ftype).data)


@requirement_module.route("requirement/alter", name="requirement_set")
class SetRequirement(APIView):

    @any_exception_throws_400
    @use_serializer(Serializer=RequirementSerializer, pass_in='data')
    def post(self, payload, format=None):
        fulfilled = Requirement.objects.filter(hospital_id=payload['hospital_id'], disease_id=payload['disease_id'])
        if fulfilled.count():
            fulfilled.delete()
        mentioned_types = payload['types']
        obsolete = map(lambda o: o.id, filter(lambda o: o.obsolete, mentioned_types))
        will_use = map(lambda o: o.id, filter(lambda o: not o.obsolete, mentioned_types))
        created = Requirement.objects.create(
            hospital_id=payload['hospital_id'],
            disease_id=payload['disease_id'],
            require_list=RequirementSerializer.deserialize_types(list(will_use))
        )
        data = RequirementSerializer.from_object(created).data

        return JsonResponse({
            'obsolete_types': list(obsolete),
            'created': data,
        })


@requirement_module.route("requirement/(?<hospital>.+?)/(?<disease>.+?)", name="requirement_get")
class GetRequirement(APIView):

    @any_exception_throws_400
    def get(self, request, hospital, disease, format=None):
        l = Requirement.objects.filter(hospital_id=hospital, disease_id=disease)
        assert l.count() == 1
        obj = l[0]

        data = RequirementSerializer.from_object(obj).validated_data

        return JsonResponse(dict(
            data,
            types=list(map(lambda o: o.id, filter(lambda o: not o.obsolete, data['types']))))
        )


urlpatterns = requirement_module.urlpatterns

