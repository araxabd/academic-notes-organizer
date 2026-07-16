from django.urls import path
from . import views

app_name = "marketplace"

urlpatterns = [
        path('', views.course_public_list, name="course_public_list"),
]
