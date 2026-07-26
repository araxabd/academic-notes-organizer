from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course
from notes.models import Note

User = get_user_model()

class CourseAuthTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="jalal", password="passwd123")
        self.course = Course.objects.create(title="Test Course", desc="This is a TestCourse", owner=self.user)
        self.note = Note.objects.create(title="Test Note", desc="This is a TestNote", content="content", course=self.course, owner=self.user)
    
    def test_course_list_by_anonymous(self):
        response = self.client.get(reverse("courses:detail", args=[self.course.id]))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('courses:detail', args=[self.course.id])}")

    def test_course_detail_by_anonymous(self):
        response = self.client.get(reverse("notes:detail", args=[self.note.id]))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('notes:detail', args=[self.note.id])}")

    def test_course_create_by_anonymous(self):
        response = self.client.get(reverse("notes:create", args=[self.course.id]))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('notes:create', args=[self.course.id])}")

    def test_course_update_by_anonymous(self):
        response = self.client.get(reverse("notes:update", args=[self.note.id]))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('notes:update', args=[self.note.id])}")

    def test_course_delete_by_anonymous(self):
        response = self.client.get(reverse("notes:delete", args=[self.note.id]))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('notes:delete', args=[self.note.id])}")
