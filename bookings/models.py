from django.db import models
from django.conf import settings

class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_landscape = models.ImageField(upload_to='accommodations/')
    image_portrait = models.ImageField(upload_to='accommodations/')

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.accommodation.name}"
