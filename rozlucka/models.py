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


class Puzzle(Model):
    name = CharField(max_length=255)
    question = TextField(max_length=255)
    answer = ForeignKey('Answer', on_delete=PROTECT)


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