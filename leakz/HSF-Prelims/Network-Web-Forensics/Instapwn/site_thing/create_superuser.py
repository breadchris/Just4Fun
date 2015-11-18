import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instagram.settings")
django.setup()

from app.models import Post, Comment, InstagramUser

user = InstagramUser.objects.create_superuser("admin", "rickisonaroll@gmail.com", "admin")

user.is_admin = True
user.save()

