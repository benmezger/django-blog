from django.contrib import admin
from django.db import models

from martor.widgets import AdminMartorWidget

from blog.models import Post, NavBarLink
from blog.forms import TagForm


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "created")
    list_filter = ("status", "tags")
    search_fields = ("title", "content")
    formfield_overrides = {models.TextField: {"widget": AdminMartorWidget}}

    form = TagForm


@admin.register(NavBarLink)
class NavBarLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created", "enabled")
    search_fields = ("title",)
