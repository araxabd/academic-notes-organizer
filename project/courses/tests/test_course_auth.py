from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()

class CourseAuthTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="jalal", password="passwd123")
        self.course = Course.objects.create(title="Test Course", desc="This is a TestCourse", owner=self.user)
    
    def test_course_list_by_anonymous(self):
        response = self.client.get(reverse("courses:list"))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('courses:list')}")

    def test_course_detail_by_anonymous(self):
        response = self.client.get(reverse("courses:detail", args=[self.course.id]))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('courses:detail', args=[self.course.id])}")

    def test_course_create_by_anonymous(self):
        response = self.client.get(reverse("courses:create"))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('courses:create')}")

    def test_course_update_by_anonymous(self):
        response = self.client.get(reverse("courses:update", args=[self.course.id]))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('courses:update', args=[self.course.id])}")

    def test_course_delete_by_anonymous(self):
        response = self.client.get(reverse("courses:delete", args=[self.course.id]))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('courses:delete', args=[self.course.id])}")
