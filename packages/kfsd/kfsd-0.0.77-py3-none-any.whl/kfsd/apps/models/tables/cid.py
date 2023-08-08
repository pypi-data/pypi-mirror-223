from kfsd.apps.models.tables.id import ID


# Collection Reference Table
class CID(ID):
    class Meta:
        app_label = "models"
        verbose_name = "CID"
        verbose_name_plural = "CID"
