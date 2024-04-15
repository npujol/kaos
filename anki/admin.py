from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.decorators import display
from unfold.widgets import UnfoldAdminColorInputWidget

from anki.models import AnkiCard, AnkiUser, CardStatus
from kaos.sites import custom_admin_site

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(Group)


@admin.register(PeriodicTask, site=custom_admin_site)
class PeriodicTaskAdmin(ModelAdmin):
    pass


@admin.register(IntervalSchedule, site=custom_admin_site)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule, site=custom_admin_site)
class CrontabScheduleAdmin(ModelAdmin):
    pass


@admin.register(SolarSchedule, site=custom_admin_site)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule, site=custom_admin_site)
class ClockedScheduleAdmin(ModelAdmin):
    pass


@admin.register(AnkiUser, site=custom_admin_site)
class AnkiUserAdmin(ModelAdmin):
    list_display = [
        "display_header",
        "display_created",
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Important dates"), {"fields": ("created_at", "updated_at")}),
    )
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    @display(description=_("User"), header=True)
    def display_header(self, instance: AnkiUser):
        return instance.username

    @display(description=_("Created"))
    def display_created(self, instance: AnkiUser):
        return instance.created_at


@admin.register(AnkiCard, site=custom_admin_site)
class AnkiCardAdmin(SimpleHistoryAdmin, ModelAdmin):
    search_fields = ["word"]
    list_filter_submit = True
    list_display = [
        "display_header",
        "display_status",
    ]
    radio_fields = {"status": admin.VERTICAL}
    readonly_fields = ["data"]

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        return form

    @display(description=_("AnkiCard"), header=True)
    def display_header(self, instance: AnkiCard):
        return [
            instance.word,
        ]

    @display(
        description=_("Status"),
        label={
            CardStatus.INACTIVE: "danger",
            CardStatus.ACTIVE: "success",
        },
    )
    def display_status(self, instance: AnkiCard):
        if instance.status:
            return instance.status

        return None
