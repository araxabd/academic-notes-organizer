from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from django.core.paginator import Paginator
from courses.models import Course
from .models import Rating, Comment

def course_public_list(request):
    courses = Course.objects.filter(is_public=True).annotate(rating=Avg("ratings__score"))
    paginator = Paginator(courses, 5)
    page_number = request.GET.get('page')
    page_courses = paginator.get_page(page_number)
    return render(request, 'marketplace/course_public_list.html', {'courses': page_courses})

def course_public_profile(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_public=True)
    notes = course.notes.filter(is_public=True).only("title", "desc", "created", "updated").order_by("created")
    return render(request, 'marketplace/course_public_profile.html', {'course': course, 'notes': notes})
