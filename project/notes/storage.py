import os
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

class NoteFileStorage(FileSystemStorage):
    def get_valid_name(self, name):
        ext = os.path.splitext(name)[1]
        timestamp = timezone.now().strftime("%Y%m%d%H%M%S%f")
        return f'{timestamp}{ext}'

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            file_name, ext = os.path.splitext(name)
            counter = 1
            while True:
                new_name = f"{file_name}_{counter}{ext}"
                if not self.exists(new_name):
                    return new_name
                counter += 1
        return name
