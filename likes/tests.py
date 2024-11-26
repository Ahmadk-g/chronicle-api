from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from posts.models import Post
from likes.models import Like


class LikeListViewTests(APITestCase):
    def setUp(self):
        """
        Create two users and one post for testing.
        """
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.brian = User.objects.create_user(username='brian',
                                              password='pass')
        self.post = Post.objects.create(
            owner=self.adam,
            title='Test Post',
            content='Content of the test post.'
        )

    def test_can_list_likes(self):
        """
        Ensure that a list of likes can be retrieved.
        """
        Like.objects.create(owner=self.adam, post=self.post)
        response = self.client.get('/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_logged_in_user_can_like_post(self):
        """
        Ensure a logged-in user can like a post.
        """
        self.client.login(username='brian', password='pass')
        response = self.client.post('/likes/', {'post': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_user_cannot_like_post_twice(self):
        """
        Ensure a user cannot like the same post twice.
        """
        self.client.login(username='adam', password='pass')
        self.client.post('/likes/', {'post': self.post.id})
        response = self.client.post('/likes/', {'post': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('possible duplicate', response.data['detail'])

    def test_user_not_logged_in_cannot_like_post(self):
        """
        Ensure a user must be logged in to like a post.
        """
        response = self.client.post('/likes/', {'post': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LikeDetailViewTests(APITestCase):
    def setUp(self):
        """
        Create two users, one post, and one like for testing.
        """
        self.adam = User.objects.create_user(username='adam', password='pass')
        self.brian = User.objects.create_user(username='brian',
                                              password='pass')
        self.post = Post.objects.create(
            owner=self.adam,
            title='Test Post',
            content='Content of the test post.'
        )
        self.like = Like.objects.create(owner=self.adam, post=self.post)

    def test_can_retrieve_like_using_valid_id(self):
        """
        Ensure a like can be retrieved using a valid ID.
        """
        response = self.client.get(f'/likes/{self.like.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'adam')

    def test_cannot_retrieve_like_using_invalid_id(self):
        """
        Ensure a like cannot be retrieved with an invalid ID.
        """
        response = self.client.get('/likes/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_delete_their_like(self):
        """
        Ensure the owner of a like can delete it.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete(f'/likes/{self.like.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)

    def test_non_owner_cannot_delete_like(self):
        """
        Ensure a user cannot delete someone else's like.
        """
        self.client.login(username='brian', password='pass')
        response = self.client.delete(f'/likes/{self.like.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_not_logged_in_cannot_delete_like(self):
        """
        Ensure a user must be logged in to delete a like.
        """
        response = self.client.delete(f'/likes/{self.like.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
