from django.db import models

from django_extensions.db.models import TimeStampedModel


class Genre(TimeStampedModel):
    name = models.CharField(max_length=100, null=False, blank=False)

    artist = models.ForeignKey(
        "music.Artist",
        null=True,
        on_delete=models.SET_NULL,
        related_name="related_genres",
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class Artist(TimeStampedModel):
    name = models.CharField(max_length=200, null=False, blank=False)

    spotify_url = models.URLField(null=False, blank=True)
    tidal_url = models.URLField(null=False, blank=True)
    lastfm_url = models.URLField(null=False, blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"

    @property
    def genres(self):
        return self.related_genres.all()
