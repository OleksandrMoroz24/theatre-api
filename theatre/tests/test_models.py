from django.test import TestCase

from theatre.models import Actor, Genre, TheatreHall, Play


class TheatreModelsTestCase(TestCase):
    def setUp(self):
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.genre = Genre.objects.create(name="Drama")
        self.theatre_hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        self.play = Play.objects.create(title="Funny Bones", description="A hilarious journey")
        self.play.actors.add(self.actor)
        self.play.genres.add(self.genre)

    def test_actor_creation(self):
        self.assertEqual(self.actor.first_name, "John")
        self.assertEqual(self.actor.last_name, "Doe")
        expected_full_name = "John Doe"
        self.assertEqual(self.actor.full_name, expected_full_name)

    def test_genre_creation(self):
        self.assertEqual(self.genre.name, "Drama")
        self.assertEqual(str(self.genre), "Drama")

    def test_theatrehall_creation(self):
        self.assertEqual(self.theatre_hall.name, "Main Hall")
        self.assertEqual(self.theatre_hall.rows, 10)
        self.assertEqual(self.theatre_hall.seats_in_row, 20)
        expected_capacity = 200  # 10 rows * 20 seats per row
        self.assertEqual(self.theatre_hall.capacity, expected_capacity)

    def test_play_creation(self):
        self.assertEqual(self.play.title, "Funny Bones")
        self.assertEqual(self.play.description, "A hilarious journey")
        self.assertIn(self.actor, self.play.actors.all())
        self.assertIn(self.genre, self.play.genres.all())
        self.assertEqual(str(self.play), "Funny Bones")
