from taggit_labels.widgets import LabelWidget


class ContentForm(forms.ModelForm):
    tags = TagField(required=False, widget=LabelWidget)
