from django.conf import settings
from django.db import models
from rest_framework.exceptions import ValidationError


class Actor(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Genre(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class TheatreHall(models.Model):
    name = models.CharField(max_length=63)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Play(models.Model):
    title = models.CharField(max_length=63)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name="plays")
    genres = models.ManyToManyField(Genre, related_name="plays")

    def __str__(self):
        return self.title


class Performance(models.Model):
    show_time = models.DateTimeField()
    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE,
        related_name="performances"
    )
    theatre_hall = models.ForeignKey(
        TheatreHall,
        on_delete=models.CASCADE,
        related_name="performances"
    )

    def __str__(self):
        return f"{self.play.title} {self.show_time}"

    class Meta:
        ordering = ["-show_time", ]


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations"
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(
        Performance,
        related_name="tickets",
        on_delete=models.CASCADE
    )
    reservation = models.ForeignKey(
        Reservation,
        related_name="tickets",
        on_delete=models.CASCADE
    )

    @staticmethod
    def validate_ticket(
        row: int,
        seat: int,
        theatre_hall: TheatreHall,
        exc_to_raise: type[Exception],
    ) -> None:
        for ticket_attr_name, ticket_attr_value, theatre_hall_attr_name in (
            ("row", row, "rows"),
            ("seat", seat, "seats_in_row"),
        ):
            max_value = getattr(theatre_hall, theatre_hall_attr_name)
            if not (1 <= ticket_attr_value <= max_value):
                raise exc_to_raise(
                    f"{ticket_attr_name} must be in range [1, {max_value}]"
                )

    def clean(self) -> None:
        self.validate_ticket(
            self.row,
            self.seat,
            self.performance.theatre_hall,
            ValidationError,
        )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ("performance", "row", "seat")
        ordering = ("row", "seat")

    def __str__(self) -> str:
        return f"{self.performance} (row: {self.row}, seat: {self.seat})"
