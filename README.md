# Running

Install node dependencies with `cd jsbuild` and `npm install`.

Run `cd jsbuild` and `npm run tailwind-watch`.

Install python dependencies with `pip install -r requirements.txt`.

Set up database and apply migrations with `python manage.py migrate`.

Create an admin with `python manage.py creatsuperuser`.

Collect static files (configure location with the `STATIC_ROOT` setting) with `python manage.py collectstatic`.

Put your images in ./guestbook/static/images/ and then run `python manage.py processimages`.

Then run the Django development server as usual `python manage.py runserver`.

____

Built with [FirstPrinciplesDevelopment/django-daisy](https://github.com/FirstPrinciplesDevelopment/django-daisy).
Uses [TailwindCSS](https://tailwindcss.com/) and [DaisyUI](https://daisyui.com/).
