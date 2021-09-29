from meta.serializers import APIMetadata
from rest_framework.response import Response
from rest_framework.decorators import action


class MetadataMixin():
    @action(detail=True, methods=['get'])
    def meta(self, request, pk):
        metadata_generator = APIMetadata()
        metadata = metadata_generator.get_serializer_info(
            self.serializer_class())
        return Response(metadata)
