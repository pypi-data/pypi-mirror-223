from django.db import models
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)


from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.constants import NAME_REGEX_CONDITION


class ID(BaseModel):
    class Meta:
        abstract = True

    name = models.CharField(
        max_length=MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=NAME_REGEX_CONDITION,
                message="name doesnt match condition {}".format(NAME_REGEX_CONDITION),
            ),
            MaxLengthValidator(MAX_LENGTH),
            MinLengthValidator(MIN_LENGTH),
        ],
    )
    slug = models.SlugField()
    attrs = models.JSONField(default=dict)
