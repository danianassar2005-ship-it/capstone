# StoryWeave

## CS50W Final Project

StoryWeave is a web application that I built using Django for my CS50W final project.

The main idea of the website is collaborative storytelling. A user can create a story and write the first chapter. Other users can then continue the story. A chapter can have more than one continuation, so the story can go in different directions.

For example:

Chapter 1
- Chapter 2A
- Chapter 2B
- Chapter 2C

This means that users can choose different branches instead of following only one story path.

---

## Why I Made StoryWeave

I wanted to make something different from a normal blogging or social media website. I liked the idea of collaborative writing and allowing more than one person to contribute to the same story.

I also wanted to create a website where the same story can have different possible paths depending on how users continue it.

---

## Distinctiveness and Complexity

StoryWeave is different from the previous CS50W projects because it is a collaborative storytelling website. The main idea is not just to create and read stories, but to allow different users to continue the same story.

The main feature of the project is the branching story system. A chapter can have multiple continuations, and each continuation can have its own continuations. This creates different paths inside the same story.

For example:

Chapter 1
- Chapter 2A
- Chapter 2B
- Chapter 2C

Chapter 2A can then have:

- Chapter 3A
- Chapter 3B

I implemented this using the `parent_chapter` field in the Chapter model. It is a self-referencing foreign key, which connects a chapter to another chapter from the same model.

Another part of the project is the Story Path feature. When a user opens a chapter, the application follows the `parent_chapter` relationships and displays the path from the first chapter to the current chapter. This helps the user understand which branch they are currently reading.

The project also has story status management. A story can be either Ongoing or Completed. The author can end a story, which prevents users from adding new continuations. The author can also reopen the story later.

Other features such as authentication, comments, saved stories, profiles, search, and genre filtering are also included in the project.

---

## Main Features

### User Accounts

Users can register, log in, and log out.

Django's built-in User model is used for the authentication system.

Some features, such as creating stories, continuing stories, saving stories, and writing comments, require the user to be logged in.

---

### Creating Stories

Logged-in users can create a new story.

When creating a story, the user enters:

- Story title
- Description
- Genre

The user who creates the story becomes the author of the story.

---

### Chapters and Branches

After creating a story, the author can write the first chapter.

Other users can continue a chapter by creating a new chapter. A chapter can have multiple continuations, so users can choose different paths for the story.

For example:

Chapter 1 - The Key

    - Search the House
    - Ask Her Brother
    - Ignore the Key

This allows different users to take the story in different directions.

---

### Story Path

When reading a chapter, the website shows the path that leads to the current chapter.

For example:

Chapter 1 - The Key
-> Search the House
-> The Storage Room

This helps the user understand which branch they are currently reading.

---

### Ending a Story

The author of a story can end the story by clicking the "End Story" button.

A story has two possible statuses:

- Ongoing
- Completed

When a story is completed, users cannot add new continuations.

The author can also click "Reopen Story" if they want to allow users to continue the story again.

---

### Explore Stories

The Explore page shows the stories available on the website.

Users can search for stories by title and filter them by genre.

The genres used in the project include:

- Fantasy
- Mystery
- Romance
- Horror
- Science Fiction
- Adventure
- Drama

---

### Save Stories

Logged-in users can save stories that they like.

Saved stories appear in the "My Library" page.

A user cannot save the same story more than once.

This feature allows users to easily come back to saved stories and check for new updates.

---

### Comments

Users who are logged in can write comments on chapters.

Each comment shows the username, the comment, and the date and time it was created.

---

### Profile

Each logged-in user has a Profile page.

The profile shows the username and the stories created by that user.

---

## JavaScript

I also used JavaScript in the project for a confirmation message when the author wants to end a story.

When the author clicks "End Story", JavaScript asks:

"Are you sure you want to end this story?"

If the user clicks Cancel, the form is not submitted.

The JavaScript code is stored in:

`stories/static/stories/script.js`

---

## Database Models

The project uses several Django models.

### Genre

The Genre model stores the different genres available for stories.

It contains a `name` field.

### Story

The Story model stores the main information about each story.

It contains:

- title
- description
- author
- genre
- status
- created_at

### Chapter

The Chapter model stores the chapters of each story.

It contains:

- story
- author
- parent_chapter
- title
- content
- created_at

The `parent_chapter` field is a self-referencing foreign key. It connects a chapter to the chapter that came before it and is used to create the branching structure.

### SavedStory

The SavedStory model stores the stories that users save to their library.

It connects a user with a story.

A unique constraint prevents the same user from saving the same story more than once.

### Comment

The Comment model stores comments written by users on chapters.

It connects a user with a chapter and stores the comment content and creation time.

---

## Files

### `manage.py`

This is the main Django command-line file. It is used to run the server, migrations, and tests.

### `config/`

This folder contains the main project settings.

`settings.py` contains the Django configuration.

`urls.py` connects the main URLs to the stories application.

`asgi.py` and `wsgi.py` are used for running the Django application.

### `stories/models.py`

This file contains all the database models for StoryWeave.

### `stories/views.py`

This file contains the main logic of the application.

It handles things such as:

- Login and registration
- Creating stories
- Creating chapters
- Continuing stories
- Comments
- Saving stories
- Searching
- Story status
- Profiles

### `stories/urls.py`

This file contains the URLs for the different pages and actions in the application.

### `stories/admin.py`

This file registers the models with the Django admin interface.

### `stories/tests.py`

This file contains automated tests for different features of the website.

### `stories/templates/stories/`

This folder contains the HTML pages.

Some of the main pages are:

- `home.html`
- `explore.html`
- `story_detail.html`
- `chapter_detail.html`
- `continue_story.html`
- `create_story.html`
- `create_chapter.html`
- `library.html`
- `profile.html`
- `login.html`
- `register.html`

### `stories/static/stories/style.css`

This file contains the CSS used to style the website and make it responsive.

### `stories/static/stories/script.js`

This file contains the JavaScript used in the project.

---

## How to Run the Project

First, create and activate a virtual environment.

On macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install all the required packages:

```bash
pip install -r requirements.txt
```

Apply the database migrations:

```bash
python3 manage.py migrate
```

Run the development server:

```bash
python3 manage.py runserver
```

Then open the URL shown in the terminal in a web browser.

For example:

```text
http://127.0.0.1:8000/
```

---

## Testing

To run the automated tests:

```bash
python3 manage.py test
```

To check the project for common Django errors:

```bash
python3 manage.py check
```

---

## Responsive Design

The website is designed to work on both desktop and smaller screens. The CSS includes responsive rules for the navigation bar, story cards, forms, and other parts of the website.