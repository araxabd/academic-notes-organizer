from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course
from notes.models import Note, Tag

User = get_user_model()

class NotePermissionTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="jalal", password="passwd123")
        self.other = User.objects.create_user(username="ghasem", password="passwd123")
        self.course = Course.objects.create(title="Test Course", desc="This is a TestCourse", owner=self.owner)
        self.note = Note.objects.create(title="Test Note", desc="This is a TestNote", content="Content", course=self.course, owner=self.owner)
        self.tag = Tag.objects.create(name="test tag")

    def test_note_read_by_other(self):
        self.client.login(username="ghasem", password="passwd123")
        response = self.client.get(reverse("notes:detail", args=[self.note.id]))
        self.assertEqual(response.status_code, 404)

    def test_note_update_by_other(self):
        self.client.login(username="ghasem", password="passwd123")
        response = self.client.post(reverse("notes:update", args=[self.note.id]), {
            'title': "New",
            'desc': "this is New",
            'content': 'new',
            'is_public': True,
            'tags': self.tag.id
            })
        self.assertEqual(response.status_code, 404)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Test Note")

    def test_note_delete_by_other(self):
        self.client.login(username="ghasem", password="passwd123")
        response = self.client.post(reverse("notes:delete", args=[self.note.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())

    def tset_course_list_by_other(self):
        other_course = Course.objects.create(title="Another", desc="Other's Course", owner=self.other)
        Note.objects.create(title="Another Note", desc="Other's Note", content="content", course=other_course,owner=self.other)
        self.client.login(username="jalal", password="passwd123")
        response = self.client.get(reverse("courses:detail", args=[self.course.id]))
        notes = response.context["notes"]
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0], self.note)
