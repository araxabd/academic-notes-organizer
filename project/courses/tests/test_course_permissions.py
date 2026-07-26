from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()

class CoursePermissionTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="jalal", password="passwd123")
        self.other = User.objects.create_user(username="ghasem", password="passwd123")
        self.course = Course.objects.create(title="Test Course", desc="This is a TestCourse", owner=self.owner)

    def test_course_read_by_other(self):
        self.client.login(username="ghasem", password="passwd123")
        response = self.client.get(reverse("courses:detail", args=[self.course.id]))
        self.assertEqual(response.status_code, 404)

    def test_course_update_by_other(self):
        self.client.login(username="ghasem", password="passwd123")
        response = self.client.post(reverse("courses:update", args=[self.course.id]), {
            'title': "New",
            'desc': "this is New",
            'is_public': True,
            'price': 50
            })
        self.assertEqual(response.status_code, 404)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Test Course")

    def test_course_delete_by_other(self):
        self.client.login(username="ghasem", password="passwd123")
        response = self.client.post(reverse("courses:delete", args=[self.course.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Course.objects.filter(id=self.course.id).exists())

    def tset_course_list_by_other(self):
        Course.objects.create(title="Another", desc="Other's Course", owner=self.other)
        self.client.login(username="jalal", password="passwd123")
        response = self.client.get(reverse("courses:list"))
        courses = response.context["courses"]
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0], self.course)
