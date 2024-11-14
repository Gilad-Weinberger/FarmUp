from django.db import models
from users.models import User
import random
import string

class Field(models.Model):
    field_id = models.CharField(unique=True, max_length=10, null=True, blank=True)
    name = models.TextField()
    crop = models.CharField(max_length=200)
    farmer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.farmer} | {self.crop}"
    
    def save(self, *args, **kwargs):
        if not self.field_id:
            self.field_id = self.generate_unique_field_id()
        super().save(*args, **kwargs)
    
    def generate_unique_field_id(self):
        characters = string.ascii_uppercase + string.digits
        while True:
            random_id = ''.join(random.choices(characters, k=10))  # generate 10-character ID
            if not Field.objects.filter(field_id=random_id).exists():  # Ensure uniqueness
                return random_id

class Line(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    line_number = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.field} | Line {self.line_number}"

class FieldActivity(models.Model):
    activity_id = models.CharField(unique=True, max_length=5, null=True, blank=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.activity_id:
            self.activity_id = self.generate_unique_activity_id()
        super().save(*args, **kwargs)
    
    def generate_unique_activity_id(self):
        characters = string.ascii_uppercase + string.digits
        while True:
            random_id = ''.join(random.choices(characters, k=5))
            if not FieldActivity.objects.filter(activity_id=random_id).exists():
                return random_id

class LineActivity(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    field_activity = models.ForeignKey(FieldActivity, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    output = models.PositiveIntegerField(null=True, blank=True)

class UserActivity(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)