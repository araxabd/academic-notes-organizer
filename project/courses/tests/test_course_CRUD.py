from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()

class CourseCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jalal", password="passwd123")
        self.client.login(username="jalal", password="passwd123")

    def test_course_create_by_user(self):
        response = self.client.post(reverse('courses:create'), {
            'title': "Test Course",
            'desc': "This course is just created for test and there is no other purpose for it.\n it is a test course",
            'is_public': False,
            'price': 0
            })
        self.assertRedirects(response, reverse("courses:list"))
        self.assertEqual(Course.objects.count(), 1)
        course = Course.objects.first()

        self.assertEqual(course.title, "Test Course")
        self.assertEqual(course.owner, self.user)

    def test_course_read_by_user(self):
        course = Course.objects.create(title="Test Course", desc="This is a TestCourse", owner=self.user)
        response = self.client.get(reverse("courses:detail", args=[course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["course"], course)

    def test_course_update_by_user(self):
        course = Course.objects.create(title="Test Course", desc="This is a TestCourse", owner=self.user)
        response = self.client.post(reverse("courses:update", args=[course.id]), {
            'title': 'New Test Course',
            "desc": "This is a NewTestCourse",
            "is_public": True,
            "price": 50
            })
        self.assertRedirects(response, reverse("courses:detail", args=[course.id]))
        course.refresh_from_db()
        self.assertEqual(course.title, "New Test Course")
        self.assertEqual(course.desc, "This is a NewTestCourse")
        self.assertTrue(course.is_public)
        self.assertEqual(course.price, 50)

    def test_course_delete_by_user(self):
        course = Course.objects.create(title="Test Course", desc="This is a TestCourse", owner=self.user)
        response = self.client.post(reverse("courses:delete", args=[course.id]))
        self.assertRedirects(response, reverse("courses:list"))
        self.assertFalse(Course.objects.filter(id=course.id).exists())


