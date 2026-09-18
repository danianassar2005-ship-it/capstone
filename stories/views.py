from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Story, Chapter, Genre, SavedStory, Comment


def home(request):
    return render(request, "stories/home.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if not username or not password:
            return render(
                request,
                "stories/register.html",
                {"error": "Please fill in all fields."}
            )

        if password != confirmation:
            return render(
                request,
                "stories/register.html",
                {"error": "Passwords do not match."}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "stories/register.html",
                {"error": "Username already exists."}
            )

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect("home")

    return render(request, "stories/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "stories/login.html",
            {"error": "Invalid username or password."}
        )

    return render(request, "stories/login.html")


def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("home")


def explore(request):
    stories = Story.objects.all().order_by("-created_at")
    genres = Genre.objects.all()

    search = request.GET.get("search")
    genre_id = request.GET.get("genre")

    if search:
        stories = stories.filter(title__icontains=search)

    if genre_id:
        stories = stories.filter(genre_id=genre_id)

    return render(
        request,
        "stories/explore.html",
        {
            "stories": stories,
            "genres": genres,
            "search": search,
            "selected_genre": genre_id,
        }
    )


def story_detail(request, story_id):
    story = get_object_or_404(
        Story,
        id=story_id
    )

    chapters = story.chapters.filter(
        parent_chapter=None
    )

    return render(
        request,
        "stories/story_detail.html",
        {
            "story": story,
            "chapters": chapters,
        }
    )


def chapter_detail(request, story_id, chapter_id):
    story = get_object_or_404(
        Story,
        id=story_id
    )

    chapter = get_object_or_404(
        Chapter,
        id=chapter_id,
        story=story
    )

    continuations = chapter.continuations.all().order_by(
        "created_at"
    )

    comments = chapter.comments.all().order_by(
        "created_at"
    )

    path = []
    current = chapter

    while current:
        path.insert(0, current)
        current = current.parent_chapter

    return render(
        request,
        "stories/chapter_detail.html",
        {
            "story": story,
            "chapter": chapter,
            "continuations": continuations,
            "comments": comments,
            "path": path,
        }
    )


@login_required
def continue_story(request, story_id, chapter_id):
    story = get_object_or_404(
        Story,
        id=story_id
    )

    parent_chapter = get_object_or_404(
        Chapter,
        id=chapter_id,
        story=story
    )

    if story.status == "completed":
        return redirect(
            "story_detail",
            story_id=story.id
        )

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if title and content:
            Chapter.objects.create(
                story=story,
                author=request.user,
                parent_chapter=parent_chapter,
                title=title,
                content=content
            )

            return redirect(
                "chapter_detail",
                story_id=story.id,
                chapter_id=parent_chapter.id
            )

    return render(
        request,
        "stories/continue_story.html",
        {
            "story": story,
            "parent_chapter": parent_chapter,
        }
    )


@login_required
def create_story(request):
    genres = Genre.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        genre_id = request.POST.get("genre")

        if title and description:
            genre = None

            if genre_id:
                genre = get_object_or_404(
                    Genre,
                    id=genre_id
                )

            story = Story.objects.create(
                title=title,
                description=description,
                author=request.user,
                genre=genre
            )

            return redirect(
                "story_detail",
                story_id=story.id
            )

    return render(
        request,
        "stories/create_story.html",
        {
            "genres": genres
        }
    )


@login_required
def create_chapter(request, story_id):
    story = get_object_or_404(
        Story,
        id=story_id
    )

    if request.user != story.author:
        return redirect(
            "story_detail",
            story_id=story.id
        )

    if story.status == "completed":
        return redirect(
            "story_detail",
            story_id=story.id
        )

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if title and content:
            Chapter.objects.create(
                story=story,
                author=request.user,
                title=title,
                content=content,
                parent_chapter=None
            )

            return redirect(
                "story_detail",
                story_id=story.id
            )

    return render(
        request,
        "stories/create_chapter.html",
        {
            "story": story
        }
    )


@login_required
def save_story(request, story_id):
    story = get_object_or_404(
        Story,
        id=story_id
    )

    SavedStory.objects.get_or_create(
        user=request.user,
        story=story
    )

    return redirect(
        "story_detail",
        story_id=story.id
    )


@login_required
def library(request):
    saved_stories = SavedStory.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "stories/library.html",
        {
            "saved_stories": saved_stories
        }
    )


@login_required
def add_comment(request, story_id, chapter_id):
    story = get_object_or_404(
        Story,
        id=story_id
    )

    chapter = get_object_or_404(
        Chapter,
        id=chapter_id,
        story=story
    )

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Comment.objects.create(
                user=request.user,
                chapter=chapter,
                content=content
            )

    return redirect(
        "chapter_detail",
        story_id=story.id,
        chapter_id=chapter.id
    )


@login_required
def profile(request):
    stories = Story.objects.filter(
        author=request.user
    ).order_by("-created_at")

    return render(
        request,
        "stories/profile.html",
        {
            "stories": stories
        }
    )


@login_required
def toggle_story_status(request, story_id):
    story = get_object_or_404(
        Story,
        id=story_id
    )

    if request.user != story.author:
        return redirect(
            "story_detail",
            story_id=story.id
        )

    if story.status == "ongoing":
        story.status = "completed"
    else:
        story.status = "ongoing"

    story.save()

    return redirect(
        "story_detail",
        story_id=story.id
    )