from django.http import Http404
from django.views.generic import FormView
from django.shortcuts import render
from django.urls import reverse

from .forms import PuzzleForm
from .models import Puzzle


class PuzzleView(FormView):
    def get_puzzle(self):
        try:
            return Puzzle.objects.get(pk=self.kwargs['puzzle_id'])
        except Puzzle.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(PuzzleView, self).get_context_data(**kwargs)
        context['puzzle'] = self.get_puzzle()
        context['correct'] = context['puzzle'].is_correct()
        return context


class PuzzleDetailView(PuzzleView):
    template_name = 'puzzle_detail.html'
    form_class = PuzzleForm

    def get_success_url(self):
        puzzle = self.get_puzzle()
        return reverse('puzzle_detail', kwargs={ 'puzzle_id': puzzle.id })

    def form_valid(self, form):
        form.save(self.get_puzzle())
        return super().form_valid(form)


class PuzzleSkipView(PuzzleView):
    pass
