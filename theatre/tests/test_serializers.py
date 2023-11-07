from django.test import TestCase

from theatre.models import Actor
from theatre.serializers import ActorSerializer


class ActorSerializerTestCase(TestCase):
    def setUp(self):
        self.actor_attributes = {"first_name": "John", "last_name": "Doe"}
        self.actor = Actor.objects.create(**self.actor_attributes)
        self.serializer = ActorSerializer(instance=self.actor)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["id", "first_name", "last_name", "full_name"]))

    def test_full_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['full_name'], 'John Doe')

    def test_serializer_creates_valid_actor(self):
        new_actor_data = {"first_name": "Jane", "last_name": "Smith"}
        new_actor_serializer = ActorSerializer(data=new_actor_data)
        if new_actor_serializer.is_valid():
            new_actor = new_actor_serializer.save()
            self.assertEqual(new_actor.first_name, "Jane")
            self.assertEqual(new_actor.last_name, "Smith")
        else:
            self.fail(f"Serializer data was not valid: {new_actor_serializer.errors}")
