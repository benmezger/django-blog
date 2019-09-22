from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import mark_safe

from martor.widgets import AdminMartorWidget

from blog.models import Post, NavBarLink
from blog.forms import TagForm

admin.site.site_header = "Ben Mezger's admin panel"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "is_published",
        "created",
        "has_related_navlink",
        "live_url",
    )

    list_filter = ("status", "tags")
    search_fields = ("title", "content")
    formfield_overrides = {models.TextField: {"widget": AdminMartorWidget}}

    form = TagForm

    def is_published(self, obj):
        return obj.status == Post.PUBLISHED_STATUS

    is_published.boolean = True

    def live_url(self, obj):
        return mark_safe(f"<a href='{obj.absolute_url}'>👀</a>")

    live_url.short_description = "View live"
    live_url.allow_tags = True

    def has_related_navlink(self, obj):
        return bool(obj.has_related_navlink)

    has_related_navlink.short_description = "Has navlink"
    has_related_navlink.boolean = True

    def delete_model(self, request, obj):
        try:
            return super().delete_model(request, obj)
        except ValidationError:
            messages.set_level(request, messages.ERROR)
            messages.error(
                request, f"Cannot delete {obj.title}. Post is linked to the Navbar."
            )


@admin.register(NavBarLink)
class NavBarLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created", "enabled")
    search_fields = ("title",)
