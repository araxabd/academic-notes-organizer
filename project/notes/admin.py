from django.contrib import admin
from .models import Note, NoteFile, Tag

admin.site.register(Note)
admin.site.register(NoteFile)
admin.site.register(Tag)
