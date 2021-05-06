from django.contrib import admin
from . models import *


class MeAdmin(admin.ModelAdmin):
    list_display = ["user"]


class ProjectAdmin(admin.ModelAdmin):
    list_display = "title software_used url updated created".split()
    list_filter = "software_used created updated".split()


admin.site.register(Me, MeAdmin)
admin.site.register(Project, ProjectAdmin)

