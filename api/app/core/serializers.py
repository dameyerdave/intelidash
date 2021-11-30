from rest_framework.serializers import (
    BaseSerializer, ModelSerializer, HiddenField, CurrentUserDefault)
from core.models import (Entry, OwnedModel, EntryType, Source, Strand,
                         Interpretation, MapEntryType, MapEntry, MapLayer, MapDrawing, Mission)
from datetime import datetime as dt


class OwnedModelSerializer(ModelSerializer):
    # url = HyperlinkedIdentityField(view_name='', read_only=True)
    owner = HiddenField(default=CurrentUserDefault())
    createdDate = HiddenField(default=dt.now())

    class Meta:
        model = OwnedModel
        abstract = True


class MissionSerializer(OwnedModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'


class StrandSerializer(OwnedModelSerializer):
    class Meta:
        model = Strand
        fields = '__all__'


class SourceSerializer(OwnedModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class EntryTypeSerializer(OwnedModelSerializer):
    class Meta:
        model = EntryType
        fields = '__all__'


class InterpretationSerializer(OwnedModelSerializer):
    class Meta:
        model = Interpretation
        fields = '__all__'


class MapEntrySerializer(OwnedModelSerializer):
    class Meta:
        model = MapEntry
        fields = '__all__'


class MapEntryGeoJsonSerializer(BaseSerializer):
    def to_representation(self, instance):
        print('--instance--', instance.entries.first().map_entry.type.icon)
        return {
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    instance.longitude,
                    instance.latitude
                ]
            },
            'properties': {
                'label': instance.entries.first().title if instance.entries.count() > 0 else '',
                'icon': f"http://localhost:8000/media/{instance.entries.first().map_entry.type.icon}" if instance.entries.count() > 0 and instance.entries.first().map_entry and instance.entries.first().map_entry.type else None
            },
            'type': 'Feature',
            'id': instance.id
        }


class MapEntryTypeSerializer(OwnedModelSerializer):
    class Meta:
        model = MapEntryType
        fields = '__all__'


class MapLayerSerializer(OwnedModelSerializer):
    class Meta:
        model = MapLayer
        fields = '__all__'


class MapDrawingGeoJsonSerializer(BaseSerializer):
    def to_representation(self, instance):
        return {
            'geometry': instance.geometry,
            'properties': instance.properties,
            'type': 'Feature',
            'id': instance.id
        }


class MapDrawingSerializer(OwnedModelSerializer):
    class Meta:
        model = MapDrawing
        fields = '__all__'


class EntrySerializer(OwnedModelSerializer):
    # mission = MissionSerializer()
    # type = EntryTypeSerializer()
    # strand = StrandSerializer()
    # source = SourceSerializer()
    # map_entry = MapEntrySerializer()

    class Meta:
        model = Entry
        fields = '__all__'
        # depth = 1
