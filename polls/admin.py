from django.contrib import admin
from .models import PollSession, Question, Option, Vote  # <-- use PollSession, not Session

admin.site.register(PollSession)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Vote)
