from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from events.models import Event


class EventListViewTests(APITestCase):
    def setUp(self):
        """
        Create test users and events for testing.
        """
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.brian = User.objects.create_user(username='brian',
                                              password='pass')
        self.event = Event.objects.create(
            owner=self.adam,
            title='Test Event',
            description='Description of the test event.',
            ticket_price=10.00,
            event_date='2024-12-31',
            start_time='18:00:00',
            end_time='22:00:00',
            location='Test Location',
            category='meetup'
        )

    def test_can_list_events(self):
        """
        Ensure that a list of events can be retrieved.
        """
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_logged_in_user_can_create_event(self):
        """
        Ensure a logged-in user can create an event.
        """
        self.client.login(username='brian', password='pass')
        response = self.client.post('/events/', {
            'title': 'New Event',
            'description': 'New event description.',
            'ticket_price': 15.00,
            'event_date': '2024-12-01',
            'start_time': '14:00:00',
            'end_time': '18:00:00',
            'location': 'New Location',
            'category': 'concert'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)

    def test_user_not_logged_in_cannot_create_event(self):
        """
        Ensure a user must be logged in to create an event.
        """
        response = self.client.post('/events/', {
            'title': 'Unauthorized Event',
            'description': 'Should not be created.',
            'ticket_price': 20.00,
            'event_date': '2024-12-01',
            'start_time': '10:00:00',
            'end_time': '12:00:00',
            'location': 'Unauthorized Location',
            'category': 'seminar'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EventDetailViewTests(APITestCase):
    def setUp(self):
        """
        Create test users and events for testing.
        """
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.brian = User.objects.create_user(username='brian',
                                              password='pass')
        self.event = Event.objects.create(
            owner=self.adam,
            title='Test Event',
            description='Description of the test event.',
            ticket_price=10.00,
            event_date='2024-12-31',
            start_time='18:00:00',
            end_time='22:00:00',
            location='Test Location',
            category='meetup'
        )

    def test_can_retrieve_event_using_valid_id(self):
        """
        Ensure an event can be retrieved using a valid ID.
        """
        response = self.client.get(f'/events/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Event')

    def test_cannot_retrieve_event_using_invalid_id(self):
        """
        Ensure an event cannot be retrieved with an invalid ID.
        """
        response = self.client.get('/events/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_update_their_event(self):
        """
        Ensure the owner of an event can update it.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.put(f'/events/{self.event.id}/', {
            'title': 'Updated Event',
            'description': 'Updated description.',
            'ticket_price': 20.00,
            'event_date': '2024-12-31',
            'start_time': '18:00:00',
            'end_time': '23:00:00',
            'location': 'Updated Location',
            'category': 'conference'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Updated Event')

    def test_non_owner_cannot_update_event(self):
        """
        Ensure a non-owner cannot update another user's event.
        """
        self.client.login(username='brian', password='pass')
        response = self.client.put(f'/events/{self.event.id}/', {
            'title': 'Unauthorized Update',
            'description': 'Should not work.',
            'ticket_price': 50.00,
            'event_date': '2024-12-31',
            'start_time': '18:00:00',
            'end_time': '23:00:00',
            'location': 'Unauthorized Location',
            'category': 'workshop'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_their_event(self):
        """
        Ensure the owner of an event can delete it.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete(f'/events/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)

    def test_non_owner_cannot_delete_event(self):
        """
        Ensure a non-owner cannot delete another user's event.
        """
        self.client.login(username='brian', password='pass')
        response = self.client.delete(f'/events/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_not_logged_in_cannot_delete_event(self):
        """
        Ensure a user must be logged in to delete an event.
        """
        response = self.client.delete(f'/events/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CategoryChoicesViewTests(APITestCase):
    def test_can_retrieve_category_choices(self):
        """
        Ensure the category choices endpoint returns valid data.
        """
        response = self.client.get('/category_choices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(Event.CATEGORY_CHOICES))
