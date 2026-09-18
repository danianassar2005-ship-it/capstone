from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Story(models.Model):
    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stories"
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stories"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ongoing"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name="chapters"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chapters"
    )
    parent_chapter = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="continuations"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.story.title} - {self.title}"


class SavedStory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="saved_stories"
    )
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name="saved_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "story"],
                name="unique_saved_story"
            )
        ]

    def __str__(self):
        return f"{self.user.username} saved {self.story.title}"


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"