from rest_framework.serializers import ModelSerializer


class ExtraFieldsMixin(ModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super().get_field_names(
            declared_fields, info)
        print('expanded_fields', expanded_fields)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
