from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from courses.models import Course
from marketplace.models import Comment

User = get_user_model()

class MarketplaceCommentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jalal", password="passwd123")
        self.public_course = Course.objects.create(title="Test Course", desc="This is a TestCourse", is_public=True, owner=self.user)
        self.private_course = Course.objects.create(title="Private Course", desc="This is a PrivateCourse", is_public=False, owner=self.user)

    def test_marketplace_comment_anonymous(self):
        response = self.client.post(reverse("marketplace:course_public_profile", args=[self.public_course.id]), {
            'content': 'this is my comment',
            'comment_submit': ''
            })
        self.assertEqual(Comment.objects.count(), 0)

    def test_marketplace_comment_private(self):
        self.client.login(username="jalal", password="passwd123")
        response = self.client.post(reverse("marketplace:course_public_profile", args=[self.private_course.id]), {
            'content': 'this is my comment',
            'comment_submit': ''
            })
        self.assertEqual(Comment.objects.count(), 0)

    def test_marketplace_comment(self):
        self.client.login(username="jalal", password="passwd123")
        response = self.client.post(reverse("marketplace:course_public_profile", args=[self.public_course.id]), {
            'content': 'this is my comment',
            'comment_submit': ''
            })
        self.assertEqual(Comment.objects.count(), 1)
        response = self.client.get(reverse("marketplace:course_public_profile", args=[self.public_course.id]))
        comments = response.context['comments']
        self.assertEqual(len(comments), 1)
        comment = Comment.objects.first()
        self.assertEqual(comments[0], comment)
