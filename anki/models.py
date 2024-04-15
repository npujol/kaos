from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from kaos.encoders import PrettyJSONEncoder


class AnkiUser(models.Model):
    username = models.CharField(_("username"), max_length=255)
    password = models.CharField(_("password"), max_length=255)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username


class CardStatus(models.TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    INACTIVE = "INACTIVE", _("Inactive")


class AnkiCard(models.Model):
    word = models.CharField(_("first name"), max_length=255)
    audio = models.FileField(
        _("audio"),
        upload_to="audio/",
        null=True,
        blank=True,
    )
    status = models.CharField(
        _("status"),
        choices=CardStatus.choices,
        null=True,
        blank=True,
        max_length=255,
    )
    data = models.JSONField(
        _("data"),
        null=True,
        blank=True,
        encoder=PrettyJSONEncoder,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    objects = HistoricalRecords()  # type: ignore

    class Meta:
        db_table = "ankicards"
        verbose_name = _("anki card")
        verbose_name_plural = _("anki cards")

    def __str__(self):
        return self.word
