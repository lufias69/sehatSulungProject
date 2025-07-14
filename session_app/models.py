from django.db import models
from django.contrib.auth.models import User

from fitur_app.models import CheckupGroup, Feature
from question_app.models import Question, Choice

class Session(models.Model):  # Ganti 'Misi' menjadi 'Session'
    checkup_group = models.ForeignKey(CheckupGroup, on_delete=models.CASCADE, related_name='sessions')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Session {self.id} for {self.checkup_group.user.username}'


class UserResponse(models.Model):
    session = models.ForeignKey(Session, related_name='responses', on_delete=models.CASCADE)  # Relasi dengan Session saja
    question = models.ForeignKey(Question, related_name='responses', on_delete=models.CASCADE)
    answer_text = models.TextField(null=True, blank=True)  # Untuk jawaban esai
    multiple_choice_answers = models.ManyToManyField(Choice, blank=True, related_name='responses_multiple_choice')

    def __str__(self):
        return f"Response for {self.question.question_text} in session {self.session.id}"
