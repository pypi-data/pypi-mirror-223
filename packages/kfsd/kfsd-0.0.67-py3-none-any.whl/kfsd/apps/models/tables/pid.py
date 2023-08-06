from kfsd.apps.models.tables.id import ID


# Project Reference Table
class PID(ID):
    class Meta:
        app_label = "models"
        verbose_name = "PID"
        verbose_name_plural = "PID"
