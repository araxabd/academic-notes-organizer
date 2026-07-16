from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
        path('list/', views.course_list, name='list'),
        path('<int:course_id>/', views.course_detail, name='detail'),
        path('create/', views.course_create, name='create'),
        path('update/<int:course_id>', views.course_update, name="update"),
        path('delete/<int:course_id>', views.course_delete, name="delete")
]
