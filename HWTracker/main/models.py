from django.db import models

class Task(models.Model):
    subject = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    description = models.TextField()
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.subject} - {self.topic}'
    def get_absolute_url(self):
        return f"/task/{self.id}/"
    class Meta:
        ordering = ['due_date']