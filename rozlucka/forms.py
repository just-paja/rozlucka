from django import forms

from .models import AnswerAttempt

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
            correct=puzzle.is_correct(answer),
        )

class StationSkipForm(forms.Form):
    pass
