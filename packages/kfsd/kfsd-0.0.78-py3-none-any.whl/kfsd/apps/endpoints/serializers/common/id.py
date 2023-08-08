from rest_framework import serializers
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)
from django.utils.translation import gettext_lazy as _

from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH
from kfsd.apps.models.constants import NAME_REGEX_CONDITION
from kfsd.apps.endpoints.serializers.common.model import BaseModelSerializer


class IDModelSerializer(BaseModelSerializer):
    identifier = serializers.CharField(read_only=False)
    slug = serializers.SlugField(read_only=False)
    name = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
            RegexValidator(
                NAME_REGEX_CONDITION,
                message=_(
                    "Only alpha numeric and spaces are allowed, regex: {}".format(
                        NAME_REGEX_CONDITION
                    )
                ),
                code="invalid_name",
            ),
        ],
    )
    attrs = serializers.JSONField(default=dict)
