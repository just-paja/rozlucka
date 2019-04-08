from django.contrib.admin import ModelAdmin, register
from .models import Answer, Attempt, Puzzle, Station, Game

@register(Answer)
class AnswerAdmin(ModelAdmin):
    pass

@register(Attempt)
class AttemptAdmin(ModelAdmin):
    pass

@register(Puzzle)
class PuzzleAdmin(ModelAdmin):
    pass

@register(Station)
class StationAdmin(ModelAdmin):
    pass

@register(Game)
class GameAdmin(ModelAdmin):
    pass
