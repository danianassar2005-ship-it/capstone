from django.test import TestCase
from django.contrib.auth.models import User

from .models import Story, Chapter, Genre, SavedStory, Comment


class StoryWeaveTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpass123"
        )

        self.genre = Genre.objects.create(
            name="Mystery"
        )

        self.story = Story.objects.create(
            title="Test Story",
            description="A test story",
            author=self.user,
            genre=self.genre
        )

        self.chapter = Chapter.objects.create(
            story=self.story,
            author=self.user,
            title="Chapter 1",
            content="This is the first chapter."
        )


    def test_home_page(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)


    def test_explore_page(self):

        response = self.client.get("/stories/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Story")


    def test_story_detail(self):

        response = self.client.get(
            f"/stories/{self.story.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Story")
        self.assertContains(response, "Chapter 1")


    def test_chapter_detail(self):

        response = self.client.get(
            f"/stories/{self.story.id}/chapters/{self.chapter.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chapter 1")


    def test_login(self):

        login = self.client.login(
            username="testuser",
            password="testpass123"
        )

        self.assertTrue(login)


    def test_save_story(self):

        self.client.login(
            username="testuser",
            password="testpass123"
        )

        response = self.client.get(
            f"/stories/{self.story.id}/save/"
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            SavedStory.objects.filter(
                user=self.user,
                story=self.story
            ).exists()
        )


    def test_library(self):

        SavedStory.objects.create(
            user=self.user,
            story=self.story
        )

        self.client.login(
            username="testuser",
            password="testpass123"
        )

        response = self.client.get(
            "/stories/library/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Story")


    def test_continue_story(self):

        self.client.login(
            username="testuser2",
            password="testpass123"
        )

        response = self.client.post(
            f"/stories/{self.story.id}/chapters/{self.chapter.id}/continue/",
            {
                "title": "Chapter 2",
                "content": "This continues the story."
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Chapter.objects.filter(
                title="Chapter 2",
                parent_chapter=self.chapter
            ).exists()
        )


    def test_add_comment(self):

        self.client.login(
            username="testuser2",
            password="testpass123"
        )

        response = self.client.post(
            f"/stories/{self.story.id}/chapters/{self.chapter.id}/comment/",
            {
                "content": "This is a great chapter!"
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Comment.objects.filter(
                user=self.user2,
                chapter=self.chapter,
                content="This is a great chapter!"
            ).exists()
        )


    def test_search(self):

        response = self.client.get(
            "/stories/?search=Test"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Story")


    def test_genre_filter(self):

        response = self.client.get(
            f"/stories/?genre={self.genre.id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Story")