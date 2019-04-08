from django import forms

class PuzzleForm(forms.Form):
    answer = forms.CharField(
        label='Odpověď',
        max_length=255,
    )

    def save(self):
        print(self)
