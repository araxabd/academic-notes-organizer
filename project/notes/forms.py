from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("title", "desc", "content","is_public", "tags")


class MultipleFileWidget(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    widget = MultipleFileWidget

    def clean(self, data, initial=None):
        if not data:
            return []

        if isinstance(data, (list, tuple)):
            return [super().clean(file,initial) for file in data]

        return [super().clean(data, initial)]
class NoteFileForm(forms.Form):
    files = MultipleFileField(required=False)
