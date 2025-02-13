# django-daisy
A template repo for Django projects with [TailwindCSS](https://tailwindcss.com/) and [DaisyUI](https://daisyui.com/).


It uses [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/index.html) and [django-browser-reload](https://pypi.org/project/django-browser-reload/) for development.

# Running

Install node dependencies with `cd jsbuild` and `npm install`.

Run `cd jsbuild` and `npm run tailwind-watch`.

Install python dependencies with `pip install -r requirements.txt`.

Set up database and apply migrations with `python manage.py migrate`.

Create an admin with `python manage.py creatsuperuser`.

Put your images in ./guestbook/static/images/ and then run `python manage.py processimages`.

Then run the Django development server as usual `python manage.py runserver`.