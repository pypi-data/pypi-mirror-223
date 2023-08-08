from kfsd.apps.models.tables.id import ID


# User Reference Table
class UID(ID):
    class Meta:
        app_label = "models"
        verbose_name = "UID"
        verbose_name_plural = "UID"
