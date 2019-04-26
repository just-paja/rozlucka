from django.contrib.admin import ModelAdmin, register
from .models import (
    Answer,
    AnswerAttempt,
    Puzzle,
    Station,
    StationFacilitator,
    StationFacilitatorGuess,
)

@register(Answer)
class AnswerAdmin(ModelAdmin):
    list_display = (
        'text',
        'puzzle',
    )

@register(AnswerAttempt)
class AnswerAttemptAdmin(ModelAdmin):
    list_display = (
        'id',
        'puzzle',
        'text',
        'created_at',
    )

@register(Puzzle)
class PuzzleAdmin(ModelAdmin):
    list_display = (
        'name',
        'is_answered',
    )

@register(StationFacilitator)
class StationFacilitatorAdmin(ModelAdmin):
    list_display = (
        'name',
        'station',
    )

@register(StationFacilitatorGuess)
class StationFacilitatorGuessAdmin(ModelAdmin):
    list_display = (
        'text',
        'station',
        'correct',
    )

@register(Station)
class StationAdmin(ModelAdmin):
    list_display = (
        'name',
        'time',
        'puzzle',
        'is_answered',
        'visited',
        'skipped',
        'next'
    )
