# Blog System

A blog website built with Django. Users can sign up, write posts, and leave comments. The site also uses machine learning to make the blog smarter.

## Features

**Blog basics**
- Sign up, log in, and log out
- Profile page with a profile picture
- Create, edit, and delete your own posts
- Pages are split into groups of 5 posts
- See all posts by one author
- Reset your password by email
- Admin panel to manage users, posts, and comments

**Machine learning features**
- **Related posts:** each post shows other posts that are similar to it.
- **Auto tags:** tags like `#django` are made from the post text. Click a tag to see all posts with it.
- **Smart search:** finds posts by meaning, not only by exact words. For example, "Italian meal" can find a post about pasta.
- **Comment moderation:** a toxicity model checks every comment. Rude comments are held back, and only their author can see them. An admin can approve them later.
- **Post summaries:** long posts get a short TL;DR made from their most important sentences.

## Tech used

- Python and Django
- SQLite database
- Bootstrap 4 and Django Crispy Forms
- scikit-learn (related posts and tags)
- sentence-transformers, model `all-MiniLM-L6-v2` (search and summaries)
- Hugging Face transformers, model `unitary/toxic-bert` (comment moderation)

## How to run

1. Create and start a virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install the packages:

   ```
   pip install -r requirements.txt
   ```

3. Set up the database:

   ```
   python manage.py migrate
   ```

4. Create tags, search data, and summaries for posts that already exist:

   ```
   python manage.py build_ml
   ```

5. Create an admin account (optional):

   ```
   python manage.py createsuperuser
   ```

6. Start the server:

   ```
   python manage.py runserver
   ```

Open http://127.0.0.1:8000 in your browser.

**Note:** the first time you save a post or write a comment, the app downloads the ML models. This needs internet and can take a few minutes. After that, they are stored on your computer.

## Run the tests

```
python manage.py test
```

## Good to know

- **Password reset emails** are printed in the terminal, not sent to a real inbox. This is set in `BlogSystem/settings.py`. Change `EMAIL_BACKEND` to use a real email service.
- **If the toxicity model cannot load** (for example, you are offline), new comments are held for review. Nothing rude gets through.
- **Moderation strictness** can be changed with `THRESHOLD` in `blog/moderation.py`. A lower number holds more comments.
- Search and related posts check every post each time, which is fine for a small blog.

## Project layout

```
BlogSystem/   project settings and main URLs
blog/         posts, comments, tags, and the ML code
  ml.py          related posts and tags
  semantic.py    smart search
  moderation.py  comment toxicity check
  summary.py     post summaries
users/        sign up, login, and profiles
```
