from django.http import Http404
from django.views.generic import FormView
from django.shortcuts import redirect
from django.urls import reverse

from .forms import PuzzleForm, StationSkipForm
from .models import Station


class PuzzleView(FormView):
    def get_station(self):
        try:
            return Station.objects.get(pk=self.kwargs['station_id'])
        except Station.DoesNotExist:
            raise Http404


    def get_status(self):
        puzzle = self.get_puzzle()
        station = self.get_station()
        if not puzzle:
            return 'no-puzzle'
        if puzzle.is_answered():
            return 'answered'
            return 'active'
        return None

    def get(self, *args, **kwargs):
        if not self.get_station().is_active():
            raise Http404
        return super(PuzzleView, self).get(*args, **kwargs)

    def get_puzzle(self):
        return self.get_station().puzzle

    def get_context_data(self, **kwargs):
        context = super(PuzzleView, self).get_context_data(**kwargs)
        context['station'] = self.get_station()
        context['puzzle'] = context['station'].puzzle
        if context['puzzle']:
            context['attempts'] = (
                context['puzzle'].answer_attempts
                .order_by('-created_at')
                .all()
            )
        else:
            context['attempts'] = []
        return context


class StationDetailView(PuzzleView):
    template_name = 'puzzle_detail.html'
    form_class = PuzzleForm

    def get_success_url(self):
        station = self.get_station()
        return reverse('station_detail', kwargs={'station_id': station.id})

    def form_valid(self, form):
        form.save(self.get_puzzle())
        return super().form_valid(form)


class StationSkipView(FormView):
    form_class = StationSkipForm


def station_visit(request, *args, **kwargs):
    try:
        station = Station.objects.get(pk=kwargs['station_id'])
    except Station.DoesNotExist:
        raise Http404

    station.visited = True
    station.save()
    return redirect(reverse('station_detail', args=[station.id]))
