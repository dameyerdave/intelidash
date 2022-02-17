### THIS SHOULD NOT BE USED BECAUSE WE CAN USE OPTIONS METHOD ###

# from meta.serializers import APIMetadata
# from rest_framework.response import Response
# from rest_framework.decorators import action

# class MetadataMixin():
#     @action(detail=False, methods=['get'])
#     def meta(self, request):
#         metadata_generator = APIMetadata()
#         metadata = metadata_generator.get_serializer_info(
#             self.serializer_class(context={'request': request}))
#         return Response(metadata)
