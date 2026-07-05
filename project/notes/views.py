from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import Note
from .forms import NoteForm

@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})

@login_required
def note_create(request, course_id):
    course = get_object_or_404(Course, id=course_id, owner=request.user)

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.course = course
            note.save()
            return redirect("notes:detail", note_id=note.id)
    else:
        form = NoteForm()
    return render(request, 'notes/note_create.html', {'form': form})
