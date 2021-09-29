from core.serializers import (EntrySerializer, EntryTypeSerializer, SourceSerializer, StrandSerializer,
                              InterpretationSerializer, MapEntrySerializer, MapEntryTypeSerializer, MapEntryGeoJsonSerializer,
                              MapLayerSerializer, MapDrawingSerializer, MapDrawingGeoJsonSerializer, MissionSerializer)
from core.models import Entry, EntryType, Source, Strand, Interpretation, MapEntry, MapEntryType, MapLayer, MapDrawing, Mission
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import IsOwnerOrAdmin
from meta.views import MetadataMixin


class StrandViewSet(ModelViewSet, MetadataMixin):
    queryset = Strand.objects.all()
    serializer_class = StrandSerializer
    permission_classes = [IsOwnerOrAdmin]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['short', 'strand']
    filterset_fields = ['mission__id']


class SourceViewSet(ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [IsOwnerOrAdmin]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['short', 'source']
    filterset_fields = ['mission__id']


class EntryTypeViewSet(ModelViewSet):
    queryset = EntryType.objects.all()
    serializer_class = EntryTypeSerializer
    permission_classes = [IsOwnerOrAdmin]


class EntryViewSet(ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsOwnerOrAdmin]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'abstract', 'content']
    filterset_fields = ['mission__id', 'strand__id', 'map_entry__id']


class InterpretationViewSet(ModelViewSet):
    queryset = Interpretation.objects.all()
    serializer_class = InterpretationSerializer
    permission_classes = [IsOwnerOrAdmin]


class MapEntryViewSet(ModelViewSet):
    queryset = MapEntry.objects.all()
    serializer_class = MapEntrySerializer
    permission_classes = [IsOwnerOrAdmin]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['layer_id', 'mission__id']

    @action(detail=False, methods=['get'])
    def geojson(self, request):
        map_entries = MapEntry.objects.all()

        serializer = MapEntryGeoJsonSerializer(map_entries, many=True)
        return Response({
            'type': 'FeatureCollection',
            'features': serializer.data
        })


class MapEntryTypeViewSet(ModelViewSet):
    queryset = MapEntryType.objects.all()
    serializer_class = MapEntryTypeSerializer
    permission_classes = [IsOwnerOrAdmin]


class MapLayerViewSet(ModelViewSet):
    queryset = MapLayer.objects.all()
    serializer_class = MapLayerSerializer
    permission_classes = [IsOwnerOrAdmin]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['mission__id']


class MapDrawingViewSet(ModelViewSet):
    queryset = MapDrawing.objects.all()
    serializer_class = MapDrawingSerializer
    permission_classes = [IsOwnerOrAdmin]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['mission__id', 'layer__id']

    @action(detail=False, methods=['get'])
    def geojson(self, request):
        map_entries = MapDrawing.objects.all()

        serializer = MapDrawingGeoJsonSerializer(map_entries, many=True)
        return Response({
            'type': 'FeatureCollection',
            'features': serializer.data
        })


class MissionViewSet(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [IsOwnerOrAdmin]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
