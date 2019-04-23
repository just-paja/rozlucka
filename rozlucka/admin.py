from django.contrib.admin import ModelAdmin, register
from .models import Answer, AnswerAttempt, Puzzle, Station, Game

@register(Answer)
class AnswerAdmin(ModelAdmin):
    pass

@register(AnswerAttempt)
class AnswerAttemptAdmin(ModelAdmin):
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
