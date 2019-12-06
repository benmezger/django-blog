from django.contrib import admin

from music.models import Genre, Artist


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    readonly_fields = ("lastfm_url", "spotify_url", "tidal_url")
