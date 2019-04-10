from django import forms

from .models import Attempt, Puzzle

class PuzzleForm(forms.Form):
    answer = forms.CharField(
        label='Odpověď',
        max_length=255,
    )

    def save(self, puzzle):
        attempt = Attempt(
            correct=self.cleaned_data['answer'] == puzzle.answer.text,
            puzzle=puzzle,
            text=self.cleaned_data['answer']
        )
        attempt.save()
