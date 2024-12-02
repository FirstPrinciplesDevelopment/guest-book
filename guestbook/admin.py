from django.contrib import admin

# Register your models here.
from .models import Visit, Visitor


class VisitAdmin(admin.ModelAdmin):
    list_display = ["visitor", "visit_datetime"]


admin.site.register(Visit, VisitAdmin)
admin.site.register(Visitor)
