from django.db import models
from accounts.models import Organizer
import uuid

class PollSession(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    join_code = models.CharField(max_length=10, unique=True, default=uuid.uuid4().hex[:6])
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    session = models.ForeignKey(PollSession, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)

class Vote(models.Model):
    session = models.ForeignKey(PollSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=100)  # Track user/device/IP
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('question', 'voter_id')  # Prevent double votes
