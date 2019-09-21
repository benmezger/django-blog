from django.forms import ModelForm

from taggit_labels.widgets import LabelWidget
from taggit.forms import TagField

from martor.fields import MartorFormField


class TagForm(ModelForm):
    tags = TagField(required=False, widget=LabelWidget)


class PostForm(ModelForm):
    description = MartorFormField()
