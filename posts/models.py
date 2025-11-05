from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_cgivk5', blank=True
    )
    artist_name = models.CharField(max_length=255, blank=True, null=True)
    year_of_artwork = models.IntegerField(blank=True, null=True)

def save(self, *args, **kwargs):
    # Call the parent save first if the object is new (so image has a path)
    if not self.pk:
        super().save(*args, **kwargs)

    if self.image:
        try:
            img = Image.open(self.image)
            img = img.convert('RGB')
            buffer = BytesIO()
            img.save(buffer, format='WEBP', quality=80)
            # Replace the file with the compressed version
            self.image.save(self.image.name, ContentFile(buffer.getvalue()), save=False)
        except Exception as e:
            print("Image compression failed:", e)

    super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'