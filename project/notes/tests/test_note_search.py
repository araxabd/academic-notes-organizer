from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from courses.models import Course
from notes.models import Note

User = get_user_model()

class NoteSearchTest(TestCase):
    def setUp(self):
        self.user  = User.objects.create_user(username="jalal", password="passwd123")
        self.client.login(username="jalal", password="passwd123")
        self.course1 = Course.objects.create(title="First", desc="fdesc", owner=self.user)
        self.course2 = Course.objects.create(title="Second", desc="sdesc", owner=self.user)
        self.note1 = Note.objects.create(title="F", desc="1", content="one", course=self.course1, owner=self.user)
        self.note2 = Note.objects.create(title="S", desc="2", content="two", course=self.course1, is_public=True,  owner=self.user)
        self.note3 = Note.objects.create(title="T", desc="3", content="three", course=self.course2, owner=self.user)

    def test_note_search_title(self):
        response = self.client.get(reverse("notes:search"), {'q': 'F'})
        notes = response.context["notes"]
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0], self.note1)

    def test_note_search_desc(self):
        response = self.client.get(reverse("notes:search"), {'q': '2'})
        notes = response.context["notes"]
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0], self.note2)

    def test_note_search_content(self):
        response = self.client.get(reverse("notes:search"), {'q': 'three'})
        notes = response.context["notes"]
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0], self.note3)

    def test_note_search_empty(self):
        response = self.client.get(reverse("notes:search"), {'q': '4'})
        notes = response.context["notes"]
        self.assertEqual(len(notes), 0)

    def test_note_filter_course(self):
        response = self.client.get(reverse("notes:search"), {'course': self.course2.id})
        notes = response.context["notes"]
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0], self.note3)

    def test_note_filter_is_public(self):
        response = self.client.get(reverse("notes:search"), {'public': 'true'})
        notes = response.context["notes"]
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0], self.note2)

    def test_note_order_old(self):
        self.note1.created = timezone.now() - timedelta(days=2)
        self.note2.created = timezone.now() - timedelta(days=1)
        self.note3.created = timezone.now()
        self.note1.save()
        self.note2.save()
        self.note3.save()

        response = self.client.get(reverse("notes:search"), {"order": "old"})
        notes = response.context["notes"]
        self.assertEqual(list(notes), [self.note1, self.note2, self.note3])
