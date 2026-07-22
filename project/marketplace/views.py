from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.core.paginator import Paginator
from courses.models import Course
from .models import Rating, Comment
from .forms import RatingForm, CommentForm

def course_public_list(request):
    courses = Course.objects.filter(is_public=True).annotate(rating=Avg("ratings__score"))
    paginator = Paginator(courses, 5)
    page_number = request.GET.get('page')
    page_courses = paginator.get_page(page_number)
    return render(request, 'marketplace/course_public_list.html', {'courses': page_courses})

def course_public_profile(request, course_id):
    course = get_object_or_404(Course.objects.annotate(rating=Avg("ratings__score")), id=course_id, is_public=True)
    rating_form = None
    comment_form = None
    if request.user.is_authenticated:
        last_rate = Rating.objects.filter(course=course, user=request.user).first()
        rating_form = RatingForm(instance=last_rate)
        comment_form = CommentForm()

    if request.method == "POST" and request.user.is_authenticated:
        if "rating_submit" in request.POST:
            rating_form = RatingForm(request.POST, instance=last_rate)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.user = request.user
                rating.course = course
                rating.save()
        elif "comment_submit" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.course = course
                comment.save()
        return redirect("marketplace:course_public_profile", course_id=course.id)
    notes = course.notes.filter(is_public=True).only("title", "desc", "created", "updated").order_by("created")
    context = {
            'course': course,
            'notes': notes,
            'rating_form': rating_form,
            'comment_form': comment_form
            }
    return render(request, 'marketplace/course_public_profile.html', context)
