from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note

@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})
