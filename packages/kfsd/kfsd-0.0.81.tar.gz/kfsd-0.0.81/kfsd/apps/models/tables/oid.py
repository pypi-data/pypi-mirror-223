from kfsd.apps.models.tables.id import ID


# Organization Reference Table
class OID(ID):
    class Meta:
        app_label = "models"
        verbose_name = "OID"
        verbose_name_plural = "OID"
