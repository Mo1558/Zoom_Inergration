from django.db import models

# Create your models here.

class Zoom(models.Model):
    meeting_id=models.IntegerField()
    created_by= models.CharField(max_length=255)
    meeting_link= models.URLField()
    password= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by