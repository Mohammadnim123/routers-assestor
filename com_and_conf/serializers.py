from rest_framework import serializers
from .services import PublicMapperService


class BaseSerializer(serializers.Serializer):
    def is_valid(self):
        return super().is_valid(raise_exception=True)
    
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ListingDataParamsSerializer(BaseSerializer):
    type = serializers.ChoiceField(choices=[(choice, choice) for choice in PublicMapperService.file_paths])
    source_company = serializers.ChoiceField(choices=[(choice, choice) for choice in PublicMapperService.all_companies])


class FieldsToChangeParamsSerializer(BaseSerializer):
    type = serializers.ChoiceField(choices=[(choice, choice) for choice in PublicMapperService.file_paths])
    command = serializers.CharField(max_length=10000)


class GetDesiredDataParamsSerializer(ListingDataParamsSerializer):
    command = serializers.CharField(max_length=10000)
    extra_fields = serializers.DictField()
    destination_company = serializers.ChoiceField(choices=[(choice, choice) for choice in PublicMapperService.all_companies])

