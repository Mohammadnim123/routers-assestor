from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import PublicMapperService
from .serializers import (ListingDataParamsSerializer, FieldsToChangeParamsSerializer,
GetDesiredDataParamsSerializer)


class PublicMapperAPIView(ViewSet, APIView):

    @action(['get'], detail=False)
    def request_type(self, request):
        request_type = PublicMapperService.request_types()
        return Response(request_type)

    @action(['get'], detail=False)
    def companies(self, request):
        exclude = request.GET.get("exclude")
        companies = PublicMapperService.companies(exclude)
        return Response(companies)

    @action(['get'], detail=False)
    def listing_data(self, request):
        params = ListingDataParamsSerializer(data=request.query_params)
        params.is_valid()
        data = PublicMapperService.listing_data(**params.data)
        return Response(data)

    @action(['post'], detail=False)
    def fields_to_change(self, request):
        params = FieldsToChangeParamsSerializer(data=request.data)
        params.is_valid()
        fields_list = PublicMapperService.fields_to_change(**params.data)
        return Response(fields_list)

    @action(['post'], detail=False)
    def get_desired_data(self, request):
        params = GetDesiredDataParamsSerializer(data=request.data)
        params.is_valid()
        fields_list = PublicMapperService.get_desired_data(**params.data)
        return Response(fields_list)