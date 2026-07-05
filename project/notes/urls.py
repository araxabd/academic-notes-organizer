from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
        path('<int:note_id>/', views.note_detail, name="detail"),
        path('course_<int:course_id>/create', views.note_create, name="create")
]
