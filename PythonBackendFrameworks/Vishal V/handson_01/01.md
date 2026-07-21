
## Step 1

To create a virutal environment 

```bash 
python -m venv venv
```

To activate the venv 

```bash 
venv/Scripts/activate
```

After activating the venv 

You will see something like this (venv) as shown below 

PS Django> python -m venv venv
PS Django> .\venv\Scripts\activate
(venv) PS Django>

## Step 2

Install Django 

```bash 
python -m pip install Django
```

(venv) PS Django> python -m pip install Django
Collecting Django
  Downloading django-6.0.6-py3-none-any.whl.metadata (3.9 kB)
Collecting asgiref>=3.9.1 (from Django)
  Downloading asgiref-3.11.1-py3-none-any.whl.metadata (9.3 kB)
Collecting sqlparse>=0.5.0 (from Django)
  Downloading sqlparse-0.5.5-py3-none-any.whl.metadata (4.7 kB)
Collecting tzdata (from Django)
  Using cached tzdata-2026.2-py2.py3-none-any.whl.metadata (1.4 kB)
Downloading django-6.0.6-py3-none-any.whl (8.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.4/8.4 MB 807.1 kB/s  0:00:10
Downloading asgiref-3.11.1-py3-none-any.whl (24 kB)
Downloading sqlparse-0.5.5-py3-none-any.whl (46 kB)
Using cached tzdata-2026.2-py2.py3-none-any.whl (349 kB)
Installing collected packages: tzdata, sqlparse, asgiref, Django
Successfully installed Django-6.0.6 asgiref-3.11.1 sqlparse-0.5.5 tzdata-2026.2

[notice] A new release of pip is available: 25.3 -> 26.1.2
[notice] To update, run: python.exe -m pip install --upgrade pip

Verify its version 

```bash 
python -m django --version
```

(venv) PS Django> python -m django --version
6.0.6

## Step 3 

Similar to npm create vite@latest coursemanager i think so,

```bash 
django-admin startproject coursemanager 
```

To start the server 
```bash 
cd coursemanager
python manage.py runserver
```

Server starts at the port 8000
```copy 
http://127.0.0.1:8000/
```

Read all the lines from the following files 

- settings.py
- urls.py 
- wsgi.py 
- agsi.py 

## Step 4 

Its  like creating a page inside a website 

```bash
python manage.py startapp courses
```

Update the settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'courses', # Add this line 
]
```

## Step 5 

I think we are creating endpoints in further steps 

Add these lines in `courses/views.py`
```python 
from django.http import HttpResponse


def hello_view(request):
    """
    Simple function-based view.
    Returns a plain text response confirming the API is running.
    Called when a GET request hits /api/hello/
    """
    return HttpResponse('Course Management API is running')
```

Create urls.py
```python 
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_view, name='hello'),
]
```

Then wire up in `coursemanager/urls.py`

```python
from django.contrib import admin
from django.urls import path, include # include include haha 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('courses.urls')),   # add this line
]
```

## Step 6

Verify 

```bash
python manage.py runserver
```

Open your browser and go to:
```
http://127.0.0.1:8000/api/hello/
```

Expected output: 
Course Management API is running


## Step 7 

Optional I think so, I did this to remove all the errors. 

(venv) PS coursemanager> python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
June 30, 2026 - 00:28:59
Django version 6.0.6, using settings 'coursemanager.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
For more information on production servers see: https://docs.djangoproject.com/en/6.0/howto/deployment/
(venv) PS coursemanager> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
(venv) PS coursemanager>

Using migrate it will store all in the `db.sqlite3` 

## Step 8 

Verify 

Performing system checks...

System check identified no issues (0 silenced).
June 30, 2026 - 00:34:10
Django version 6.0.6, using settings 'coursemanager.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
For more information on production servers see: https://docs.djangoproject.com/en/6.0/howto/deployment/

Now system says **no issues**

Simplified version 

(venv) PS coursemanager> python manage.py check
System check identified no issues (0 silenced).
(venv) PS coursemanager>

## Step 9 

```bash 
pip install django-extensions
```

To view all the urls 

Add this line in `settings.py`

```python
INSTALLED_APPS = [
    ...
    "django_extensions",
]
```
```bash 
python manage.py show_urls 
```

(venv) PS coursemanager> python manage.py show_urls
/admin/ django.contrib.admin.sites.index        admin:index
/admin/<app_label>/     django.contrib.admin.sites.app_index    admin:app_list
/admin/<url>    django.contrib.admin.sites.catch_all_view
/admin/auth/group/      django.contrib.admin.options.changelist_view    admin:auth_group_changelist
/admin/auth/group/<path:object_id>/     django.views.generic.base.RedirectView
/admin/auth/group/<path:object_id>/change/      django.contrib.admin.options.change_view        admin:auth_group_change
/admin/auth/group/<path:object_id>/delete/      django.contrib.admin.options.delete_view        admin:auth_group_delete
/admin/auth/group/<path:object_id>/history/     django.contrib.admin.options.history_view       admin:auth_group_history
/admin/auth/group/add/  django.contrib.admin.options.add_view   admin:auth_group_add
/admin/auth/user/       django.contrib.admin.options.changelist_view    admin:auth_user_changelist
/admin/auth/user/<id>/password/ django.contrib.auth.admin.user_change_password  admin:auth_user_password_change
/admin/auth/user/<path:object_id>/      django.views.generic.base.RedirectView
/admin/auth/user/<path:object_id>/change/       django.contrib.admin.options.change_view        admin:auth_user_change
/admin/auth/user/<path:object_id>/delete/       django.contrib.admin.options.delete_view        admin:auth_user_delete
/admin/auth/user/<path:object_id>/history/      django.contrib.admin.options.history_view       admin:auth_user_history
/admin/auth/user/add/   django.contrib.auth.admin.add_view      admin:auth_user_add
/admin/autocomplete/    django.contrib.admin.sites.autocomplete_view    admin:autocomplete
/admin/jsi18n/  django.contrib.admin.sites.i18n_javascript      admin:jsi18n
/admin/login/   django.contrib.admin.sites.login        admin:login
/admin/logout/  django.contrib.admin.sites.logout       admin:logout
/admin/password_change/ django.contrib.admin.sites.password_change      admin:password_change
/admin/password_change/done/    django.contrib.admin.sites.password_change_done admin:password_change_done
/admin/r/<path:content_type_id>/<path:object_id>/       django.contrib.contenttypes.views.shortcut      admin:view_on_site
/api/hello/     courses.views.hello_view        hello
(venv) PS coursemanager>

Only this is what we have created 

/api/hello/     courses.views.hello_view        hello

Other than this one all the ones ae predefined urls by admin 
