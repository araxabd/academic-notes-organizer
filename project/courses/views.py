from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Course

@login_required
def course_list(request):
    courses = Course.objects.filter(owner=request.user)
    context = {
            'courses': courses
            }
    return render(request, 'courses/course_list.html', context)
