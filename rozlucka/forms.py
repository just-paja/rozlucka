from django import forms

from .models import AnswerAttempt, StationFacilitatorGuess

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

class UnlockForm(forms.Form):
    answer = forms.CharField(
        label='Kdo hlídá tento checkpoint?',
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Napiš jeho křestní jméno nebo přezdívku'
        })
    )

    def save(self, station):
        answer = self.cleaned_data['answer']
        StationFacilitatorGuess.objects.create(
            station=station,
            text=answer,
            correct=station.is_facilitator(answer),
        )

class StationSkipForm(forms.Form):
    def save(self, station):
        station.skipped = True
        station.next.skipped = True
        station.save()
        station.next.save()
