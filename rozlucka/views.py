from django.http import Http404
from django.views.generic import FormView
from django.shortcuts import render
from django.urls import reverse

from .forms import PuzzleForm
from .models import Puzzle


class PuzzleDetailView(FormView):
    template_name = 'puzzle_detail.html'
    form_class = PuzzleForm

    def get_puzzle(self):
        try:
            return Puzzle.objects.get(pk=self.kwargs['puzzle_id'])
        except Puzzle.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(PuzzleDetailView, self).get_context_data(**kwargs)
        context['puzzle'] = self.get_puzzle()
        return context

    def get_success_url(self):
        puzzle = self.get_puzzle()
        return reverse('puzzle_detail', kwargs={ 'puzzle_id': puzzle.id })

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PuzzleSkipView(FormView):
    def get(request):
        pass
