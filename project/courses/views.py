from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import CourseForm

@login_required
def course_list(request):
    courses = Course.objects.filter(owner=request.user)
    q = request.GET.get("q", "").strip()
    from_date = request.GET.get("from")
    to_date = request.GET.get("to")
    order = request.GET.get("order")
    if q:
        courses = courses.filter(Q(title__icontains=q) | Q(desc__icontains=q))

    if from_date:
        courses = courses.filter(created__date__gte=from_date)

    if to_date:
        courses = courses.filter(created__date__lte=to_date)

    if order == "newmodify":
        courses = courses.order_by("-updated")
    elif order == "oldmodify":
        courses = courses.order_by("updated")
    elif order == "old":
        courses = courses.order_by("created")
    else:
        courses = courses.order_by("-created")


    paginator = Paginator(courses, 5)
    page_number = request.GET.get('page')
    page_courses = paginator.get_page(page_number)
    context = {
            'courses': page_courses,
            'order': order,
            'q': q
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
        return render(request, 'courses/course_update.html', { 'form': form , 'course_title': course.title})

@login_required
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id, owner=request.user)
    if request.method == "POST":
        course.delete()
        return redirect("courses:list")
    return render(request, 'courses/course_delete.html', {'course': course})
