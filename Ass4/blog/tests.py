from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Comment


class PostTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        # API endpoint for posts
        self.url = '/api/posts/'

    def test_create_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            'title': 'Test Post',
            'content': 'This is a test post content',
            'author': self.user.id,

        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post(self):
        post = Post.objects.create(
            title='Old Title',
            content='Old Content',
            author=self.user
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        data = {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'author': self.user.id
        }

        response = self.client.put(f'{self.url}{post.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_posts(self):
        Post.objects.create(title="Post 1", content="Content of post 1", author=self.user)
        Post.objects.create(title="Post 2", content="Content of post 2", author=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # We expect 2 posts to be returned

    def test_get_single_post(self):
        post = Post.objects.create(title="Single Post", content="This is a single post", author=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(f'{self.url}{post.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], post.title)
        self.assertEqual(response.data['content'], post.content)

    def test_create_post_without_auth(self):
        data = {
            'title': 'Unauthorized Post',
            'content': 'This post should not be created without authorization',
            'author': self.user.id,
        }

        # No authorization token is sent
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_with_invalid_data(self):
        post = Post.objects.create(title="Original Post", content="Original Content", author=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Missing required fields, such as title
        data = {
            'content': 'Updated Content Without Title',
            'author': self.user.id
        }

        response = self.client.put(f'{self.url}{post.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_post(self):
        post = Post.objects.create(title="Post to Delete", content="This post will be deleted", author=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.delete(f'{self.url}{post.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)  # Ensure that the post was deleted

    def test_delete_post_without_auth(self):
        post = Post.objects.create(title="Post to Delete", content="This post should not be deleted", author=self.user)

        # No token provided, this simulates unauthorized access
        response = self.client.delete(f'{self.url}{post.id}/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_without_auth(self):
        post = Post.objects.create(title="Post to Update", content="This post will be updated", author=self.user)

        # No token provided, simulating unauthorized access
        data = {
            'title': 'Updated Title Without Auth',
            'content': 'This content should not be updated without auth',
            'author': self.user.id
        }

        response = self.client.put(f'{self.url}{post.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_with_empty_content(self):
        data = {
            'title': 'Post with Empty Content',
            'content': '',
            'author': self.user.id
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post_with_long_title(self):
        long_title = 'A' * 256  # Assuming title should be within 255 characters
        data = {
            'title': long_title,
            'content': 'Content for the post with a long title',
            'author': self.user.id
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_non_existent_post(self):
        non_existent_post_id = 99999  # A post ID that does not exist
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(f'{self.url}{non_existent_post_id}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentTests(APITestCase):

    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.url = '/api/posts/'

    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='password')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        # Create a test post
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content',
            author=self.user
        )

        # API endpoints for comments
        self.comment_url = f'/api/posts/{self.post.id}/comments/'

    # Test to list comments for a post
    def test_list_comments(self):
        # Create a comment for the post
        Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment.'
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Make a GET request to list comments for the post
        response = self.client.get(self.comment_url)

        # Check that the request was successful and returns the correct status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the comment data is correct
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'This is a test comment.')

    # Test to create a comment for a post
    def test_create_comment(self):
        # Create a post to associate the comment with
        post = Post.objects.create(
            title='Test Post',
            content='This is a test post content',
            author=self.user
        )

        # Set authentication header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Prepare the data for the comment
        data = {
            'content': 'This is a test comment',
            'author': self.user.id,
            'post': post.id  # Make sure you include the post ID
        }

        # Send POST request to create the comment
        response = self.client.post(f'{self.url}{post.id}/comments/', data, format='json')

        # Assert that the response status code is HTTP_201_CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test to create a comment without authentication
    def test_create_comment_without_auth(self):
        # Define the data for the comment
        data = {
            'content': 'This comment should fail due to missing authentication.',
        }

        # Make a POST request without authentication
        response = self.client.post(self.comment_url, data, format='json')

        # Check that the request was unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
