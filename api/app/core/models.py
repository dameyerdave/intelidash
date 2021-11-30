from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey
from django.db.models import (Model, SET_NULL, CASCADE, JSONField,
                              ImageField, CharField, DateTimeField, FloatField, TextField, Manager)


class OwnedModel(Model):
    """ A base model with an owner and a createDate. """
    owner = ForeignKey(get_user_model(), null=True, on_delete=SET_NULL)
    createdDate = DateTimeField()

    class Meta:
        abstract = True


class Mission(OwnedModel):
    """The mission where all objects belong to"""
    short = CharField(max_length=10)
    name = CharField(max_length=50)
    description = TextField(blank=True)

    def __str__(self):
        return f"{self.short} ({self.name})"


class EntryType(OwnedModel):
    """ The defined entry types. """
    short = CharField(unique=True, max_length=4)
    type = CharField(max_length=50)

    def __str__(self):
        return f"{self.short} ({self.type})"


class Source(OwnedModel):
    """ The source of an entry. """
    short = CharField(unique=True, max_length=10)
    source = CharField(max_length=50)
    mission = ForeignKey(Mission, on_delete=CASCADE,
                         null=True, related_name='sources')

    def __str__(self):
        return f"{self.short} ({self.source})"


class Strand(OwnedModel):
    """ The strand of an entry. """
    short = CharField(unique=True, max_length=10)
    strand = CharField(max_length=50)
    mission = ForeignKey(Mission, on_delete=CASCADE,
                         null=True, related_name='strands')

    def __str__(self):
        return f"{self.short} ({self.strand})"


class MapEntryType(OwnedModel):
    short = CharField(max_length=10)
    type = CharField(max_length=50)
    description = TextField(blank=True)
    icon = ImageField()

    def __str__(self):
        return f"{self.short} ({self.type})"


class MapLayer(OwnedModel):
    name = CharField(max_length=50)
    strand = ForeignKey(Strand, on_delete=SET_NULL,
                        null=True, related_name='layers')
    mission = ForeignKey(Mission, on_delete=CASCADE,
                         null=True, related_name='layers')

    def __str__(self):
        return f"{self.name}"


class MapDrawing(OwnedModel):
    name = CharField(max_length=50)
    geometry = JSONField(default=dict)
    properties = JSONField(default=dict)
    layer = ForeignKey(MapLayer, on_delete=CASCADE,
                       null=True,  related_name='drawings')
    mission = ForeignKey(Mission, on_delete=CASCADE,
                         null=True, related_name='drawings')


class MapEntry(OwnedModel):
    latitude = FloatField()
    longitude = FloatField()
    short = CharField(max_length=10, null=True)
    location = CharField(max_length=50, null=True)
    description = CharField(max_length=50, null=True, blank=True)
    type = ForeignKey(MapEntryType, null=True, on_delete=SET_NULL)
    layer = ForeignKey(MapLayer, on_delete=CASCADE,
                       null=True, related_name='entries')
    mission = ForeignKey(Mission, on_delete=CASCADE,
                         null=True, related_name='mapentries')

    def __str__(self):
        return f"{self.short} ({self.description} @ {self.location})"

    """
    {
      "type": "FeatureCollection",
      "features": [
          {
              "geometry": {
                  "type": "Point",
                  "coordinates": [
                      7.483492374420166,
                      46.93365478515625
                  ]
              },
              "properties": {
                  "origin": "parcel",
                  "geom_quadindex": "02130022113",
                  "weight": 6,
                  "zoomlevel": 10,
                  "lon": 7.483492374420166,
                  "detail": "1 muri bei bern 356 ch234685356930",
                  "rank": 10,
                  "geom_st_box2d": "BOX(7.482871 46.933291,7.484117 46.934047)",
                  "lat": 46.93365478515625,
                  "num": 1,
                  "y": 46.93365478515625,
                  "x": 7.483492374420166,
                  "label": "<b>Muri bei Bern</b> 1 (CH 2346 8535 6930)",
                  "id": 341729018
              },
              "type": "Feature",
              "id": 341729018,
              "bbox": [
                  7.482871,
                  46.933291,
                  7.484117,
                  46.934047
              ]
          }
      ]
  }
    """


class EntryManager(Manager):
    def get_queryset(self):
        return super().get_queryset()


class Entry(OwnedModel):
    """ An entry (basically automatically generated). """
    type = ForeignKey(EntryType, null=True, default=None, on_delete=SET_NULL)
    source = ForeignKey(Source, null=True, default=None, on_delete=SET_NULL)
    title = CharField(max_length=255)
    abstract = TextField()
    content = TextField()
    publishedDate = DateTimeField(null=True)
    strand = ForeignKey(Strand, null=True, default=None, on_delete=SET_NULL)
    map_entry = ForeignKey(MapEntry, null=True,
                           on_delete=SET_NULL, related_name='entries')
    mission = ForeignKey(Mission, on_delete=CASCADE,
                         null=True, related_name='entries')

    objects = EntryManager()

    def __str__(self):
        return f"{self.source}: {self.title} ({self.publishedDate})"


class Interpretation(OwnedModel):
    entry = ForeignKey(Entry, on_delete=CASCADE)
    interpretation = TextField()
