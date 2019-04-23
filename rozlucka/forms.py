import unidecode

from django import forms
from .models import AnswerAttempt

from .models import AnswerAttempt, Puzzle

def is_correct(answer, attempt):
    left = unidecode.unidecode(answer).strip().lower()
    right = unidecode.unidecode(attempt).strip().lower()
    print('%s == %s' % (left, right))
    return left == right

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
            correct=is_correct(puzzle.answer.text, answer),
        )
