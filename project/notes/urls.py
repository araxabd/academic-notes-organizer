from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
        path('<int:note_id>/', views.note_detail, name="detail"),
        path('course_<int:course_id>/create', views.note_create, name="create"),
        path('update/<int:note_id>', views.note_update, name="update"),
        path('delete/<int:note_id>', views.note_delete, name="delete"),
        path('search/', views.note_search, name="search")
]
