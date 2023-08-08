from kfsd.apps.models.tables.id import ID


# Team Reference Table
class TID(ID):
    class Meta:
        app_label = "models"
        verbose_name = "TID"
        verbose_name_plural = "TID"
