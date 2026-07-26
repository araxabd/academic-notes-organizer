from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from courses.models import Course
from notes.models import Note, Tag

User = get_user_model()

class NoteTagTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jalal", password="passwd123")
        self.client.login(username="jalal", password="passwd123")
        self.course = Course.objects.create(title="Test Course", desc="This is a TestCourse", owner=self.user)
        self.tag1 = Tag.objects.create(name="first")
        self.tag2 = Tag.objects.create(name="second")
        self.note1 = Note.objects.create(title="F", desc="1", content="one", course=self.course, owner=self.user)
        self.note2 = Note.objects.create(title="S", desc="2", content="two", course=self.course, owner=self.user)
        self.note1.tags.add(self.tag1)
        self.note2.tags.add(self.tag1, self.tag2)

    def test_note_common_tag(self):
        response = self.client.get(reverse("notes:tag", args=[self.tag1]))
        notes = response.context["notes"]
        self.assertEqual(len(notes), 2)

    def test_note_individual_tag(self):
        response = self.client.get(reverse("notes:tag", args=[self.tag2]))
        notes = response.context["notes"]
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0], self.note2)
