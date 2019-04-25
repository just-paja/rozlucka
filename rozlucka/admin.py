from django.contrib.admin import ModelAdmin, register
from .models import Answer, AnswerAttempt, Puzzle, Station, Game

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

@register(Station)
class StationAdmin(ModelAdmin):
    list_display = (
        'name',
        'puzzle',
        'is_answered',
        'visited',
        'skipped',
        'next'
    )

@register(Game)
class GameAdmin(ModelAdmin):
    pass
