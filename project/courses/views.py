from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import CourseForm

@login_required
def course_list(request):
    courses = Course.objects.filter(owner=request.user)
    context = {
            'courses': courses
            }
    return render(request, 'courses/course_list.html', context)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, owner=request.user)
    notes = course.notes.all().order_by("created")
    context = {
            'course': course,
            'notes': notes
            }
    return render(request, 'courses/course_detail.html', context)

@login_required
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.save()
            return redirect('courses:list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_create.html', { 'form': form })

@login_required
def course_update(request, course_id):
    course = get_object_or_404(Course, id=course_id, owner=request.user)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
           form.save()
           return redirect('courses:list')
    else:
        form = CourseForm(instance=course)
        return render(request, 'courses/course_update.html', { 'form': form })
