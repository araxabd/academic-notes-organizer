from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course

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
