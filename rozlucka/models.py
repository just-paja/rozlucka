from datetime import datetime

import unidecode

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
        # is not skipped
        # station before is answered and not skipped
        # station before before is skipped
        if self.skipped:
            return False

        if self.is_answered():
            return True

        if not self.prev.first() or self.prev.first().is_answered():
            return True

        return False


class Game(Model):
    initial_station = ForeignKey('Station', on_delete=PROTECT)
    due = DateTimeField()
    started = BooleanField(default=False)
