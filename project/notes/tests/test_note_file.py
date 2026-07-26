import os
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from courses.models import Course
from notes.models import Note, Tag, NoteFile

User = get_user_model()

class NoteFileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jalal", password="passwd123")
        self.client.login(username="jalal", password="passwd123")
        self.course = Course.objects.create(title="Test Course", desc="This is a Test Course", owner=self.user)
        self.tag = Tag.objects.create(name="test tag")

    def test_note_good_file_in_creation(self):
        file = SimpleUploadedFile('text.txt', b'This is a text', content_type="text/plain")
        response = self.client.post(reverse("notes:create", args=[self.course.id]), {
            'title': "Test Note",
            'desc': "This is a TestNote",
            'content': "Content",
            "is_public": False,
            'tags': self.tag,
            'files': file
            })
        note = Note.objects.first()
        self.assertRedirects(response, reverse("notes:detail", args=[note.id]))
        self.assertEqual(note.files.count(), 1)
    
    def test_note_bad_file_in_creation(self):
        exec_path = os.path.join(os.path.dirname(__file__), "files", "hello")
        with open(exec_path, "rb") as f:
            file = SimpleUploadedFile('x.exe', f.read(), content_type="application/x-executable")
        response = self.client.post(reverse("notes:create", args=[self.course.id]), {
            'title': "Test Note",
            "desc": "This is a TestNote",
            "content": "Content",
            "is_public": False,
            "tags": self.tag,
            "files": file
            })
        self.assertEqual(Note.objects.count(), 0)
        self.assertEqual(NoteFile.objects.count(), 0)

