from django.db import models
from django.core.exceptions import ValidationError

from django_extensions.db.models import TimeStampedModel

from martor.models import MartorField
from taggit.managers import TaggableManager

from blog.manager import CheckBeforeDeleteManager


class AbstractBlogPage(TimeStampedModel):
    STATUS = ((0, "Draft"), (1, "Publish"))

    title = models.CharField(max_length=200, unique=True, null=False)
    slug = models.SlugField(max_length=200, unique=True, null=False)
    status = models.IntegerField(choices=STATUS, default=0)
    tags = TaggableManager()

    class Meta:
        abstract = True


class Post(AbstractBlogPage):
    allow_comments = models.BooleanField(default=True)
    content = MartorField()

    objects = CheckBeforeDeleteManager()

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.related_navlinks.count() > 0:
            raise ValidationError("Post has related navlink")
        return super().delete(*args, **kwargs)

    @property
    def has_related_navlink(self):
        return self.related_navlinks.first()


class NavBarLink(TimeStampedModel):
    title = models.CharField(max_length=200, unique=True, null=False)
    slug = models.SlugField(max_length=200, unique=True, null=False)

    post = models.ForeignKey(
        "blog.Post",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="related_navlinks",
    )

    enabled = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f"{self.title}"

    def clean(self):
        if self.post.status == "Draft":
            raise ValidationError("Post is a draft.")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
