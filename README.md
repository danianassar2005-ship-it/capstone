# StoryWeave

## CS50W Final Project

StoryWeave is a Django web application for collaborative storytelling.
Users can create stories, write starting chapters, and allow other
logged-in users to add continuations. A chapter can have multiple
continuations, so a story can develop into different branches rather
than one fixed sequence. Readers can explore stories, follow the path to
a chapter, save stories, and comment on chapters.

## Distinctiveness and Complexity

StoryWeave's central purpose is collaborative fiction built around
branching narratives. Its main content is not a collection of
independent posts: chapters are connected, and readers can choose among
continuations written by different users. Each continuation can receive
further continuations, allowing a story to develop into several possible
paths. This narrative structure determines how the data is stored,
retrieved, and displayed.

The branching system is implemented through the `parent_chapter` field
in the `Chapter` model. It is a nullable foreign key that refers to
another record of the same model. A chapter without a parent is a
starting chapter; a chapter with a parent continues that chapter. This
self-referencing relationship allows the application to represent both a
linear sequence and multiple branches from the same chapter. It also
lets the application retrieve the continuations of a specific chapter
without treating every chapter as an unrelated entry.

The chapter detail view uses the parent relationships to construct the
Story Path. It starts from the chapter being viewed, follows
`parent_chapter` repeatedly until it reaches a starting chapter, and
inserts each chapter at the beginning of a list. The template displays
the resulting sequence from the beginning to the current chapter. This
is important because a reader may enter a story at a later chapter and
needs to understand which branch led there.

The application also manages whether a story is open for contributions.
Each story has an `ongoing` or `completed` status. The author can end a
story or reopen it. The views check the status before creating the first
chapter or adding a continuation, so a completed story cannot receive
new chapters through those actions. The interface reflects the status by
showing the relevant controls and messages.

These features require several related database objects and rules to
work together. Stories are linked to their authors and optional genres.
Chapters are linked to stories and authors, and can be linked to parent
chapters. Comments belong to individual chapters, while saved stories
connect a user to a story. A unique database constraint on the
user/story pair prevents the same user from saving a story more than
once. Authentication and ownership checks distinguish actions available
to any logged-in contributor from actions reserved for the story's
author.

StoryWeave includes accounts, comments, profiles, and saved stories, but
those features support its writing workflow. The main interaction is
creating a narrative and adding or selecting a continuation, not
publishing a social feed or following other users. Its distinctiveness
comes from the branching story model and the reading and contribution
features built around that model. Its complexity comes from implementing
those relationships, reconstructing a chapter's path, and enforcing
authentication, ownership, and story-status rules across the relevant
views.

## Main Features

-   **Accounts:** Users can register, log in, and log out using Django's
    built-in `User` model.
-   **Story creation:** Logged-in users can create a story with a title,
    description, and optional genre. The creator becomes its author.
-   **Chapters and branches:** The author can write the first chapter.
    Logged-in users can add continuations to chapters while the story is
    ongoing. A chapter can have more than one continuation.
-   **Story Path:** The chapter page shows the sequence of parent
    chapters leading to the current chapter.
-   **Story status:** The author can end an ongoing story and reopen a
    completed one. Completed stories do not accept new chapters or
    continuations.
-   **Explore:** Users can browse stories, search by title, and filter
    by genre.
-   **Saved stories:** Logged-in users can save stories to My Library.
    Duplicate saves by the same user are prevented.
-   **Comments:** Logged-in users can comment on chapters. Comments
    display the username and creation time.
-   **Profile:** Users can view their username and the stories they
    created.
-   **Responsive layout:** CSS media queries adapt the navigation, story
    grid, forms, and other elements for smaller screens.

## Database Models

The application defines five models in `stories/models.py`:

-   **Genre** stores a unique genre name.
-   **Story** stores the title, description, author, optional genre,
    status, and creation time.
-   **Chapter** stores the story, author, optional parent chapter,
    title, content, and creation time. Its self-referencing parent field
    supports branching.
-   **SavedStory** connects a user and a story and stores when it was
    saved. A unique constraint prevents duplicate saves.
-   **Comment** connects a user to a chapter and stores the comment text
    and creation time.

## Files

The project is organized as a Django project named `config` and an
application named `stories`.

### Project-level files

-   **`manage.py`** is Django's command-line utility for running the
    development server, applying migrations, and running tests.
-   **`config/__init__.py`** marks the project configuration directory
    as a Python package.
-   **`config/settings.py`** contains Django configuration, including
    installed applications, middleware, templates, database, and
    static-file settings.
-   **`config/urls.py`** contains the top-level URL configuration and
    connects requests to the application.
-   **`config/asgi.py`** and **`config/wsgi.py`** provide the ASGI and
    WSGI application entry points.
-   **`requirements.txt`** lists the Python packages and versions
    required to run the project.
-   **`.gitignore`** lists local and generated files that should not be
    tracked by Git, including the virtual environment, Python bytecode,
    and operating-system metadata.
-   **`db.sqlite3`** is the local SQLite database file used by the
    project.

### Application files

-   **`stories/models.py`** defines the `Genre`, `Story`, `Chapter`,
    `SavedStory`, and `Comment` models and their database relationships.
-   **`stories/views.py`** contains the request-handling logic. It
    renders pages and handles registration, login, logout, story
    creation, first-chapter creation, continuations, comments, saving
    stories, searching, profiles, and story-status changes. It also
    checks login requirements, story ownership, and story status before
    allowing restricted actions.
-   **`stories/urls.py`** maps application URL paths to view functions
    for browsing, creating, reading, continuing, saving, commenting,
    authentication, and status changes.
-   **`stories/admin.py`** is the Django admin configuration file, where
    application models can be registered for administration.
-   **`stories/apps.py`** contains the Django application configuration.
-   **`stories/tests.py`** contains automated tests using Django's test
    framework. They cover page responses and content, login, saving and
    viewing saved stories, continuing a chapter, adding a comment, title
    search, and genre filtering.
-   **`stories/migrations/`** contains Django migration files used to
    apply model changes to the database.

### HTML templates

The templates are stored in `stories/templates/stories/`. Most extend
`base.html` to reuse the common page structure.

-   **`base.html`** defines the shared HTML layout, navigation bar,
    footer, and references to the static CSS and JavaScript files. It
    displays different navigation links depending on whether the user is
    logged in.
-   **`home.html`** displays the project introduction and links to
    Explore and story creation.
-   **`explore.html`** displays available stories and provides the
    title-search and genre-filter form.
-   **`create_story.html`** contains the form for creating a story,
    including its title, description, and optional genre.
-   **`story_detail.html`** displays story information and starting
    chapters. It also shows the author's status controls, the save
    option, and links to chapters and continuations.
-   **`create_chapter.html`** contains the form for the story author to
    write the first chapter.
-   **`chapter_detail.html`** displays chapter content, the Story Path,
    continuations, and comments. It also provides forms for continuing
    and commenting when applicable.
-   **`continue_story.html`** contains the form for adding a
    continuation to a selected parent chapter.
-   **`library.html`** displays the signed-in user's saved stories.
-   **`profile.html`** displays the signed-in user's username and
    created stories.
-   **`login.html`** contains the login form and displays authentication
    errors.
-   **`register.html`** contains the registration form and displays
    validation errors.

### Static files

-   **`stories/static/stories/style.css`** contains the website's
    styling for navigation, page layouts, story cards, forms, chapter
    content, and buttons. It also includes responsive media queries for
    smaller screens.
-   **`stories/static/stories/script.js`** contains the JavaScript
    confirmation shown when the author submits the form to end a story.
    If the user cancels, the form submission is prevented.

## How to Run the Project

These instructions are for macOS or Linux.

1.  Open a terminal and move into the project directory.

2.  Create and activate a virtual environment:

    ``` bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install the required packages:

    ``` bash
    pip install -r requirements.txt
    ```

4.  Apply the database migrations:

    ``` bash
    python3 manage.py migrate
    ```

5.  Start the development server:

    ``` bash
    python3 manage.py runserver
    ```

6.  Open `http://127.0.0.1:8000/` in a browser.

## Testing

Run the automated tests with:

``` bash
python3 manage.py test
```

Run Django's project checks with:

``` bash
python3 manage.py check
```

The tests exercise key page and feature behavior, including story
browsing, chapter display, authentication, saved stories, continuations,
comments, title search, and genre filtering.

## Additional Information

StoryWeave is intended to run locally using Django's development server.
It uses Django's built-in authentication, SQLite for the local database,
Django templates for the pages, CSS for styling, and JavaScript for the
story-ending confirmation. The documentation describes the current
implementation; features not listed here should not be assumed to be
part of the application.
