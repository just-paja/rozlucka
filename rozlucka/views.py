from django.http import Http404
from django.views.generic import FormView
from django.shortcuts import redirect
from django.urls import reverse

from .forms import PuzzleForm, StationSkipForm, UnlockForm
from .models import Station


class PuzzleView(FormView):
    def get_station(self):
        try:
            return Station.objects.get(pk=self.kwargs['station_id'])
        except Station.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        if not self.get_station().is_active():
            raise Http404
        return super(PuzzleView, self).get(request, *args, **kwargs)

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


class StationUnlockView(PuzzleView):
    template_name = 'station_unlock.html'
    form_class = UnlockForm

    def get(self, request, *args, **kwargs):
        station = self.get_station()
        if station.skipped:
            raise Http404
        if station.is_unlocked():
            return redirect(reverse('station_detail', kwargs={'station_id': station.id}))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['guesses'] = ctx['station'].facilitator_guesses.all()
        return ctx

    def get_success_url(self):
        station = self.get_station()
        target = 'station_unlock'
        if station.is_unlocked():
            target = 'station_detail'
        return reverse(target, kwargs={'station_id': station.id})

    def form_valid(self, form):
        form.save(self.get_station())
        return super().form_valid(form)


class StationDetailView(PuzzleView):
    template_name = 'puzzle_detail.html'
    form_class = PuzzleForm

    def get(self, request, *args, **kwargs):
        station = self.get_station()
        if station.skipped:
            raise Http404
        if not station.is_unlocked():
            return redirect(reverse('station_unlock', kwargs={'station_id': station.id}))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        station = self.get_station()
        return reverse('station_detail', kwargs={'station_id': station.id})

    def form_valid(self, form):
        form.save(self.get_puzzle())
        return super().form_valid(form)


class StationSkipView(PuzzleView):
    form_class = StationSkipForm
    template_name = 'station_skip.html'

    def get_success_url(self):
        station = self.get_station()
        return reverse('station_skip', kwargs={'station_id': station.id})

    def form_valid(self, form):
        form.save(self.get_station())
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = Station.objects.next_station()
        return context

def station_visit(request, *args, **kwargs):
    try:
        station = Station.objects.get(pk=kwargs['station_id'])
    except Station.DoesNotExist:
        raise Http404

    station.visited = True
    station.save()
    return redirect(reverse('station_detail', args=[station.id]))
