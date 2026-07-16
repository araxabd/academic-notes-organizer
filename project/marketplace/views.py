from django.shortcuts import render
from django.db.models import Avg
from courses.models import Course
from .models import Rating, Comment

def course_public_list(request):
    courses = Course.objects.filter(is_public=True).annotate(rating=Avg("ratings__score"))
    return render(request, 'marketplace/course_public_list.html', {'courses': courses})
