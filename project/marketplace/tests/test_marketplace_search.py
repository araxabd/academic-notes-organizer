from datetime import timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from courses.models import Course
from marketplace.models import Rating, Comment

User = get_user_model()

class MarketplaceSearchTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jalal", password="passwd123")
        self.other = User.objects.create_user(username="ghasem", password="passwd123")
        self.course1 = Course.objects.create(title="1", desc="first", is_public=True, price=0, owner=self.user)
        self.course2 = Course.objects.create(title="2", desc="second", is_public=True, price=2, owner=self.user)
        self.course3 = Course.objects.create(title="3", desc="third", is_public=True, price=3, owner=self.user)
        self.course4 = Course.objects.create(title="4", desc="fourth", is_public=True, price=4, owner=self.other)

    def test_marketplace_search_title(self):
        response = self.client.get(reverse("marketplace:course_public_list"), {'q': '1'})
        courses = response.context["courses"]
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0], self.course1)

    def test_marketplace_search_desc(self):
        response = self.client.get(reverse("marketplace:course_public_list"), {'q': 'second'})
        courses = response.context["courses"]
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0], self.course2)

    def test_marketplace_search_user(self):
        response = self.client.get(reverse("marketplace:course_public_list"), {'q': 'ghasem'})
        courses = response.context["courses"]
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0], self.course4)

    def test_marketplace_filter_min_price(self):
        response = self.client.get(reverse("marketplace:course_public_list"), {'min': '3'})
        courses = response.context["courses"]
        self.assertEqual(len(courses), 2)

    def test_marketplace_filter_max_price(self):
        response = self.client.get(reverse("marketplace:course_public_list"), {'max': '0'})
        courses = response.context["courses"]
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0], self.course1)

    def test_marketplace_order_old(self):
        self.course1.created = timezone.now() - timedelta(days=3)
        self.course2.created = timezone.now() - timedelta(days=2)
        self.course3.created = timezone.now() - timedelta(days=1)
        self.course4.created = timezone.now()
        self.course1.save()
        self.course2.save()
        self.course3.save()
        self.course4.save()

        response = self.client.get(reverse("marketplace:course_public_list"), {"order": "old"})
        courses = response.context["courses"]
        self.assertEqual(list(courses), [self.course1, self.course2, self.course3, self.course4])

