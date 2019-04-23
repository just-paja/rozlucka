from datetime import datetime
from django.db.models import (
    BooleanField,
    DateTimeField,
    ForeignKey,
    CharField,
    Model,
    CASCADE,
    PROTECT,
    TextField,
)


class Answer(Model):
    text = CharField(max_length=255)

    def __str__(self):
        return self.text


class AnswerAttempt(Model):
    text = CharField(max_length=255)
    puzzle = ForeignKey(
        'Puzzle',
        on_delete=CASCADE,
        related_name='answer_attempts',
    )
    correct = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return '%s, %s' % (self.puzzle, self.created_at)


class Puzzle(Model):
    name = CharField(max_length=255)
    question = TextField(max_length=255)
    answer = ForeignKey('Answer', on_delete=PROTECT)

    def __str__(self):
        return '%s' % self.name

    def is_answered(self):
        return self.answer_attempts.filter(correct=True).count() > 0


class Station(Model):
    name = CharField(max_length=63)
    description = TextField()
    puzzle = ForeignKey(
        'Puzzle',
        on_delete=PROTECT,
        null=True,
        blank=True,
    )
    next = ForeignKey(
        'Station',
        related_name='prev',
        null=True,
        blank=True,
        on_delete=PROTECT,
    )
    visited = BooleanField(default=False)
    skipped = BooleanField(default=False)

    def is_answered(self):
        if self.puzzle:
            return self.puzzle.is_answered()
        return False


class Game(Model):
    initial_station = ForeignKey('Station', on_delete=PROTECT)
    due = DateTimeField()
    started = BooleanField(default=False)
