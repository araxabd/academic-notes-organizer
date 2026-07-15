from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from courses.models import Course
from .models import Note, NoteFile
from .forms import NoteForm, NoteFileForm

from markdown import markdown

@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    files = NoteFile.objects.filter(owner=request.user, note=note)
    content_md = markdown(note.content)
    return render(request, 'notes/note_detail.html', {'note': note, 'content_md': content_md, 'files': files})

@login_required
def note_create(request, course_id):
    course = get_object_or_404(Course, id=course_id, owner=request.user)

    if request.method == "POST":
        note_form = NoteForm(request.POST)
        file_form = NoteFileForm(request.POST, request.FILES)
        if note_form.is_valid() and file_form.is_valid():
            note = note_form.save(commit=False)
            note.owner = request.user
            note.course = course
            note.save()
            for file in request.FILES.getlist("files"):
                note_file = NoteFile(note=note,owner=request.user,title=file.name, file=file, size=file.size)
                note_file.full_clean()
                note_file.save()
            return redirect("notes:detail", note_id=note.id)
    else:
        note_form = NoteForm()
        file_form = NoteFileForm()
    return render(request, 'notes/note_create.html', {'note_form': note_form, 'file_form': file_form})

@login_required
def note_update(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('courses:detail', course_id=note.course.id)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_update.html', {'form': form})

@login_required
def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    if request.method == "POST":
        note.delete()
        return redirect("courses:detail", course_id=note.course.id)
    return render(request, 'notes/note_delete.html', {'note': note})

@login_required
def note_search(request):
    q = request.GET.get('q', '')
    notes = Note.objects.filter(Q(owner=request.user) & ( Q(title__icontains=q) | Q(content__icontains=q) | Q(desc__icontains=q) | Q(tags__icontains=q)))
    return render(request, 'notes/note_search.html', {'notes': notes, 'searched_phrase': q})
