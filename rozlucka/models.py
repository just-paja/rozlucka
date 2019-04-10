from datetime import datetime
from django.db.models import (
    BooleanField,
    DateTimeField,
    ForeignKey,
    CharField,
    Model,
    PROTECT,
    TextField,
)


class Answer(Model):
    text = CharField(max_length=255)

    def __str__(self):
        return self.text


class Attempt(Model):
    puzzle = ForeignKey('Puzzle', on_delete=PROTECT, related_name='attempts')
    text = CharField(max_length=255)
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

    def is_correct(self):
        return self.attempts.filter(correct=True).count() > 0


class Station(Model):
    puzzle = ForeignKey('Puzzle', on_delete=PROTECT)
    next = ForeignKey(
        'Station',
        related_name='prev',
        null=True,
        blank=True,
        on_delete=PROTECT,
    )
    visited = BooleanField(default=False)
    skipped = BooleanField(default=False)


class Game(Model):
    initial_station = ForeignKey('Station', on_delete=PROTECT)
    due = DateTimeField()
    started = BooleanField(default=False)
