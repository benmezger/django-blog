from django.db import models
from django.core.exceptions import ValidationError

from django_extensions.db.models import TimeStampedModel

from martor.models import MartorField
from taggit.managers import TaggableManager


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

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.title


class NavBarLink(TimeStampedModel):
    title = models.CharField(max_length=200, unique=True, null=False)
    slug = models.SlugField(max_length=200, unique=True, null=False)

    post = models.ForeignKey(
        "blog.Post", null=True, blank=False, on_delete=models.SET_NULL
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
