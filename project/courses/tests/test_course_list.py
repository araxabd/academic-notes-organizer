from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from courses.models import Course

User = get_user_model()

class CourseListTest(TestCase):
    def setUp(self):
        self.user  = User.objects.create_user(username="jalal", password="passwd123")
        self.client.login(username="jalal", password="passwd123")
        self.course1 = Course.objects.create(title="First", desc="fdesc", owner=self.user)
        self.course2 = Course.objects.create(title="Second", desc="sdesc", owner=self.user)
        self.course3 = Course.objects.create(title="Third", desc="tdesc", owner=self.user)

    def test_course_search_title(self):
        response = self.client.get(reverse("courses:list"), {'q': 'First'})
        courses = response.context["courses"]
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0], self.course1)

    def test_course_search_desc(self):
        response = self.client.get(reverse("courses:list"), {'q': 'sdesc'})
        courses = response.context["courses"]
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0], self.course2)

    def test_course_search_empty(self):
        response = self.client.get(reverse("courses:list"), {'q': 'fourth'})
        courses = response.context["courses"]
        self.assertEqual(len(courses), 0)

    def test_course_order_old(self):
        self.course1.created = timezone.now() - timedelta(days=2)
        self.course2.created = timezone.now() - timedelta(days=1)
        self.course3.created = timezone.now()
        self.course1.save()
        self.course2.save()
        self.course3.save()

        response = self.client.get(reverse("courses:list"), {"order": "old"})
        courses = response.context["courses"]
        self.assertEqual(list(courses), [self.course1, self.course2, self.course3])
