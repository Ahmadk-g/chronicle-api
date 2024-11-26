from django.test import TestCase
from django.contrib.auth.models import User
from events.models import Event
from attendings.models import Attending
from rest_framework import status
from rest_framework.test import APITestCase


class AttendingListViewTests(APITestCase):
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
            description='Test event description.',
            event_date='2024-12-25',
            start_time='10:00:00',
            end_time='12:00:00',
            location='Test Venue',
            category='seminar',
        )

    def test_can_list_attendings(self):
        """
        Ensure that the list of attendings can be retrieved.
        """
        Attending.objects.create(
                owner=self.adam, event=self.event, status='attending')
        response = self.client.get('/attendings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_logged_in_user_can_create_attending(self):
        """
        Ensure that logged-in users can mark themselves as attending an event.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.post('/attendings/', {
            'event': self.event.id,
            'status': 'attending',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attending.objects.count(), 1)

    def test_user_not_logged_in_cannot_create_attending(self):
        """
        Ensure that unauthenticated users cannot create an attending record.
        """
        response = self.client.post('/attendings/', {
            'event': self.event.id,
            'status': 'attending',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_create_multiple_attending_marks_for_same_event(self):
        """
        Ensure that a user cannot mark attendance
        multiple times for the same event.
        """
        self.client.login(username='adam', password='pass')
        # First attendance record
        self.client.post('/attendings/', {'event': self.event.id,
                                          'status': 'attending'})
        # Second attendance record for the same event
        response = self.client.post('/attendings/', {'event': self.event.id,
                                                     'status': 'attending'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'],
                         'You have already marked attendance for this event.')


class AttendingDetailViewTests(APITestCase):
    def setUp(self):
        """
        Create test users, events, and attending records for testing.
        """
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.brian = User.objects.create_user(username='brian',
                                              password='pass')
        self.event = Event.objects.create(
            owner=self.adam,
            title='Test Event',
            description='Test event description.',
            event_date='2024-12-25',
            start_time='10:00:00',
            end_time='12:00:00',
            location='Test Venue',
            category='seminar',
        )
        self.attending_by_adam = Attending.objects.create(
            owner=self.adam,
            event=self.event,
            status='attending'
        )
        self.attending_by_brian = Attending.objects.create(
            owner=self.brian,
            event=self.event,
            status='interested'
        )

    def test_can_retrieve_attending_with_valid_id(self):
        """
        Ensure an attending record can be retrieved by a valid ID.
        """
        response = self.client.get(f'/attendings/{self.attending_by_adam.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'attending')

    def test_cannot_retrieve_attending_with_invalid_id(self):
        """
        Ensure an invalid attending ID returns a 404 error.
        """
        response = self.client.get('/attendings/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_update_their_attending_status(self):
        """
        Ensure the owner can update their attendance status.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.put(
            f'/attendings/{self.attending_by_adam.id}/', {
              'status': 'interested',
              'owner': self.adam.id,
              'event': self.event.id,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attending_by_adam.refresh_from_db()
        self.assertEqual(self.attending_by_adam.status, 'interested')

    def test_non_owner_cannot_update_attending_status(self):
        """
        Ensure a non-owner cannot update someone else's attendance status.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.put(
            f'/attendings/{self.attending_by_brian.id}/', {
              'status': 'attending'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_their_attending_record(self):
        """
        Ensure that the owner of an attendance record can delete it.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete(
            f'/attendings/{self.attending_by_adam.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Attending.objects.count(), 1)

    def test_non_owner_cannot_delete_attending_record(self):
        """
        Ensure that a non-owner cannot delete someone else's attendance record.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete(
            f'/attendings/{self.attending_by_brian.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_not_logged_in_cannot_delete_attending_record(self):
        """
        Ensure that unauthenticated users cannot delete attendance records.
        """
        response = self.client.delete(
            f'/attendings/{self.attending_by_adam.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
