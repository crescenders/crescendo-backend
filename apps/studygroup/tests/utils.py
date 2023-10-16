from django.core.files.uploadedfile import SimpleUploadedFile


def create_dummy_image(name, content_type="image/jpeg", size=1024):
    return SimpleUploadedFile(name, bytes(size), content_type)
