from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

LocationTypes = [
    ("PR", "Province"), ("DC", "District"), ("MN", "MainPlace"), ("SP", "SubPlace")
]

class Location(MPTTModel):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=2, choices=LocationTypes)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.parent)
