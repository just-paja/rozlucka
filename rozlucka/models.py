from datetime import datetime

import unidecode

from django.db.models import (
    BooleanField,
    DateTimeField,
    ForeignKey,
    CharField,
    Manager,
    Model,
    CASCADE,
    PROTECT,
    TextField,
    TimeField,
)


class Answer(Model):
    text = CharField(max_length=255)
    puzzle = ForeignKey(
        'Puzzle',
        on_delete=CASCADE,
        related_name='answers',
        null=True,
    )

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

def is_answer_correct(answer, attempt):
    left = unidecode.unidecode(answer).strip().lower()
    right = unidecode.unidecode(attempt).strip().lower()
    return left == right


class Puzzle(Model):
    name = CharField(max_length=255)
    question = TextField(max_length=255)

    def __str__(self):
        return '%s' % self.name

    def is_answered(self):
        return self.answer_attempts.filter(correct=True).count() > 0

    def count_answers(self):
        return self.answers.count()

    def is_correct(self, answer):
        for puzzle_answer in self.answers.all():
            if is_answer_correct(puzzle_answer.text, answer):
                return True
        return False


class StationFacilitator(Model):
    name = CharField(max_length=63)
    station = ForeignKey(
        'Station',
        on_delete=CASCADE,
        related_name='facilitators'
    )


class StationFacilitatorGuess(Model):
    text = CharField(max_length=63)
    station = ForeignKey(
        'Station',
        on_delete=CASCADE,
        related_name='facilitator_guesses',
    )
    correct = BooleanField(default=False)


class StationManager(Manager):
    def next_station(self):
        station = self.filter(
            next__isnull=True,
            visited=False,
        ).first()
        while station and station.next:
            if not station.skipped:
                station = station.next
        return station


class Station(Model):
    name = CharField(max_length=63)
    description = TextField()
    instructions = TextField(blank=True, null=True)
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
    time = TimeField(null=True)
    objects = StationManager()

    def __str__(self):
        return self.name

    def is_answered(self):
        if self.puzzle:
            return self.puzzle.is_answered()
        return False

    def is_facilitator(self, name):
        for facilitator in self.facilitators.all():
            if is_answer_correct(facilitator.name, name):
                return True
        return False

    def is_unlocked(self):
        return self.facilitator_guesses.filter(correct=True).count() >= 1

    def is_active(self):
        if self.is_answered():
            return True
        prev = self.prev.first()
        if not prev or prev.skipped or prev.is_answered():
            return True
        return False

    def is_skippable(self):
        return self.next and self.next.next


class Game(Model):
    initial_station = ForeignKey('Station', on_delete=PROTECT)
    due = DateTimeField()
    started = BooleanField(default=False)
