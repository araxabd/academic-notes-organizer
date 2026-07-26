from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note, Tag
from courses.models import Course

User = get_user_model()

class NoteCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jalal", password="passwd123")
        self.client.login(username="jalal", password="passwd123")
        self.course = Course.objects.create(title="Test Course", desc="This is a TestCourse", owner=self.user)
        self.tag = Tag.objects.create(name="test tag")

    def test_note_create_by_user(self):
        response = self.client.post(reverse("notes:create", args=[self.course.id]), {
            'title': "Test Note",
            'desc': "This is a TestNote",
            'content': "This is the content of the TestNote",
            'is_public': False,
            'tags': '',
            'files': ''
            })
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.first()
        self.assertRedirects(response, reverse("notes:detail", args=[note.id]))
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.course, self.course)
        self.assertEqual(note.owner, self.user)

    def test_note_read_by_user(self):
        note = Note.objects.create(title="Test Note", desc="This is a TestNote", content="Content", course=self.course, owner=self.user)
        response = self.client.get(reverse("notes:detail", args=[note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["note"], note)

    def test_note_update_by_user(self):
        note = Note.objects.create(title="Test Note", desc="This is a TestNote", content="Content", course=self.course, owner=self.user)
        response = self.client.post(reverse("notes:update", args=[note.id]), {
            'title': "New Note",
            'desc': 'This is NewNote',
            "content": "NewContent",
            'is_public': True,
            'tags': self.tag.id})
        self.assertRedirects(response, reverse("notes:detail", args=[note.id]))
        note.refresh_from_db()
        self.assertEqual(note.title, "New Note")
        self.assertTrue(note.is_public)
        self.assertEqual(note.owner, self.user)
        self.assertEqual(note.course, self.course)

    def test_note_delete_by_user(self):
        note = Note.objects.create(title="Test Note", desc="This is a TestNote", content="Content", course=self.course, owner=self.user)
        response = self.client.post(reverse("notes:delete", args=[note.id]))
        self.assertRedirects(response, reverse("courses:detail", args=[self.course.id]))
        self.assertFalse(Note.objects.filter(id=note.id).exists())

