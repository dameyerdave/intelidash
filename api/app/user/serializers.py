from rest_framework.exceptions import ValidationError as ValidationException
from rest_framework.serializers import HyperlinkedModelSerializer, ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['url', 'username',
                  'password', 'email', 'is_staff', 'is_active']

    def validate_password(self, value):
        try:
            validate_password(value, get_user_model())
            return make_password(value)
        except ValidationException as ve:
            raise ValidationError(f"{_('Password validation error')}: {ve}")
