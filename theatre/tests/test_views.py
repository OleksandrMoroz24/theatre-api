from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from theatre.models import Actor, Genre, Play


class ViewSetsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = get_user_model().objects.create_superuser(
            email='superuser@email.com', password='pass')
        self.client.force_authenticate(user)
        self.actor = Actor.objects.create(first_name='John', last_name='Doe')
        self.genre = Genre.objects.create(name='Comedy')
        self.play = Play.objects.create(title='Funny Bones', description='A hilarious journey')
        self.actor_url = reverse('theatre:actor-list')
        self.genre_url = reverse('theatre:genre-list')
        self.theatre_hall_url = reverse('theatre:theatrehall-list')
        self.play_url = reverse('theatre:play-list')

    def test_actor_operations(self):
        actor_data = {'first_name': 'Jane', 'last_name': 'Smith'}
        response = self.client.post(self.actor_url, actor_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.actor_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_genre_operations(self):
        genre_data = {'name': 'Action'}
        response = self.client.post(self.genre_url, genre_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.genre_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_theatrehall_operations(self):
        theatre_hall_data = {'name': 'Small Hall', 'rows': 5, 'seats_in_row': 10}
        response = self.client.post(self.theatre_hall_url, theatre_hall_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.theatre_hall_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_bad_play_creation(self):
        play_data = {
            "title": "The Great Escape",
            "description": "An escape journey",
        }
        response = self.client.post(self.play_url, play_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.play_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
