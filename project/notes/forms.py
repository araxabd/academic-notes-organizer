from django import forms
from .models import Note
from .validators import validate_mimetype

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("title", "desc", "content","is_public") 


class NoteUpdateForm(forms.ModelForm):
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

        if not isinstance(data, (list, tuple)):
            data = [data]

        cleaned_files = []

        for file in data:
            cleaned = super().clean(file, initial)
            validate_mimetype(cleaned)
            cleaned_files.append(cleaned)

        return cleaned_files
class NoteFileForm(forms.Form):
    files = MultipleFileField(required=False)
