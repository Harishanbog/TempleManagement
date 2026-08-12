from optparse import AmbiguousOptionError
from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.user,models.admin_model)
admin.site.register(models.maasa)
admin.site.register(models.paksha)
admin.site.register(models.thithi)