from django.db import models
from audit_log.models.fields import LastUserField
from audit_log.models.managers import AuditLog

class CourseVenue(models.Model):
    title = models.CharField(max_length = 255)
    created_date = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_date = models.DateTimeField(auto_now_add = False, auto_now = True)
    active = models.BooleanField(default = True)
    street_name = models.CharField(max_length = 255)
    street_number = models.CharField(max_length = 25)
    city = models.CharField(max_length = 25)

    audit_log = AuditLog()

    def __unicode__(self):
        return u"%s - %s" %(self.title, self.city)

    def get_city(self):
        return self.city

    class Meta:
        ordering = ['updated_date']
