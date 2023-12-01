from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return "/task/%i/" % self.id
    class Meta:
        ordering = ['due_date']