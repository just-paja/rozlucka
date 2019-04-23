from django import forms
from .models import AnswerAttempt

from .models import AnswerAttempt, Puzzle

class PuzzleForm(forms.Form):
    answer = forms.CharField(
        label='Odpověď',
        max_length=255,
    )

    def save(self, puzzle):
        answer = self.cleaned_data['answer']
        AnswerAttempt.objects.create(
            puzzle=puzzle,
            text=answer,
            correct=answer == puzzle.answer.text,
        )
        attempt.save()
