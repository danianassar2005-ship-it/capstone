from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "stories/",
        views.explore,
        name="explore"
    ),

    path(
        "stories/create/",
        views.create_story,
        name="create_story"
    ),

    path(
        "stories/library/",
        views.library,
        name="library"
    ),

    path(
        "stories/<int:story_id>/save/",
        views.save_story,
        name="save_story"
    ),
    path(
    "stories/profile/",
    views.profile,
    name="profile"
    ),

    path(
        "stories/<int:story_id>/",
        views.story_detail,
        name="story_detail"
    ),

    path(
        "stories/<int:story_id>/create-chapter/",
        views.create_chapter,
        name="create_chapter"
    ),

    path(
        "stories/<int:story_id>/chapters/<int:chapter_id>/",
        views.chapter_detail,
        name="chapter_detail"
    ),

    path(
        "stories/<int:story_id>/chapters/<int:chapter_id>/continue/",
        views.continue_story,
        name="continue_story"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
    "stories/<int:story_id>/chapters/<int:chapter_id>/comment/",
    views.add_comment,
    name="add_comment"
    ),
    path(
    "stories/<int:story_id>/status/",
    views.toggle_story_status,
    name="toggle_story_status"
    ),
]