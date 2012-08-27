from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

LocationTypes = [
    ("PR", "Province"), ("DC", "District"), ("MN", "MainPlace"), ("SP", "SubPlace")
]

class Location(MPTTModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=2, choices=LocationTypes)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        a = self.name
        if self.parent:
            return "%s -> %s" % (a, self.parent)
        return a
