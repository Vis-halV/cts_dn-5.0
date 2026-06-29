# notes.py
# =============================================================
# Hands-On 1 — Task 1: Web Framework Concepts
# Django request lifecycle, middleware, WSGI vs ASGI, MVC vs MVT
# =============================================================


# =============================================================
# STEP 1: Journey of GET /api/courses/ through Django
# =============================================================
#
# 1. BROWSER sends:
#       GET /api/courses/ HTTP/1.1
#       Host: 127.0.0.1:8000
#
# 2. WSGI/ASGI SERVER (e.g. gunicorn / uvicorn) receives the
#    raw TCP request and converts it into a Python-friendly
#    environ dict, then hands it to Django.
#
# 3. MIDDLEWARE STACK (request phase — top to bottom):
#    Each middleware class in MIDDLEWARE (settings.py) gets to
#    inspect or modify the request before it reaches the view.
#    Example: SecurityMiddleware checks HTTPS headers.
#
# 4. URL ROUTER (urls.py):
#    Django reads ROOT_URLCONF from settings.py, loads urls.py,
#    and walks the urlpatterns list top-to-bottom until a
#    pattern matches '/api/courses/'.
#    If no pattern matches → 404 response.
#
# 5. VIEW (views.py):
#    The matched view function (or class-based view) is called
#    with the HttpRequest object.
#    The view contains the business logic — it decides what
#    data to fetch and how to respond.
#
# 6. MODEL / DATABASE:
#    The view calls ORM methods:
#       courses = Course.objects.all()
#    Django ORM translates this to SQL, sends it to the DB,
#    and returns QuerySet objects back to the view.
#
# 7. RESPONSE CONSTRUCTION:
#    The view builds an HttpResponse (or JsonResponse, or
#    renders a Template) and returns it.
#
# 8. MIDDLEWARE STACK (response phase — bottom to top):
#    Each middleware gets to inspect or modify the response
#    on the way back out.
#    Example: CommonMiddleware may add Content-Length header.
#
# 9. WSGI/ASGI SERVER sends the HTTP response bytes back to
#    the browser.
#
# Visual summary:
#
#  Browser
#    │  GET /api/courses/
#    ▼
#  WSGI/ASGI Server
#    │
#    ▼
#  Middleware (request phase) ──► SecurityMiddleware, SessionMiddleware ...
#    │
#    ▼
#  URL Router (urls.py)  ──► matches path → picks view function
#    │
#    ▼
#  View (views.py)  ──► calls Model/ORM
#    │                        │
#    │                        ▼
#    │                   Database (SQL)
#    │                        │
#    │◄───────── QuerySet ────┘
#    │
#    ▼
#  Response (HttpResponse / JsonResponse / rendered Template)
#    │
#    ▼
#  Middleware (response phase)
#    │
#    ▼
#  Browser receives response


# =============================================================
# STEP 2: Where Middleware sits + two built-in examples
# =============================================================
#
# Middleware sits BETWEEN the WSGI server and the URL router
# on the way in, and between the view response and the WSGI
# server on the way out. Think of it as a pipeline of
# pre-processors and post-processors.
#
# Django processes request middleware TOP → BOTTOM (as listed
# in settings.MIDDLEWARE) and response middleware BOTTOM → TOP.
#
# Two built-in Django middleware classes:
#
# 1. django.middleware.security.SecurityMiddleware
#    - Enforces HTTPS by redirecting HTTP requests when
#      SECURE_SSL_REDIRECT = True.
#    - Adds HTTP Strict Transport Security (HSTS) headers.
#    - Removes the X-Powered-By header to avoid leaking info.
#    → Protects your app from basic transport-layer attacks.
#
# 2. django.contrib.sessions.middleware.SessionMiddleware
#    - Reads the session cookie from the incoming request and
#      attaches a session object to request.session.
#    - On the way out, saves any session changes and sets the
#      Set-Cookie header in the response.
#    → Enables per-user state (login sessions, shopping carts).


# =============================================================
# STEP 3: WSGI vs ASGI
# =============================================================
#
# WSGI (Web Server Gateway Interface)
#   - The original Python web server standard (PEP 3333).
#   - Synchronous: one request is handled completely before
#     the next begins in that thread/process.
#   - Django's default: wsgi.py is the entry point.
#   - Works well for traditional request-response web apps.
#   - Servers: gunicorn, uWSGI.
#
# ASGI (Asynchronous Server Gateway Interface)
#   - The modern async-capable Python standard.
#   - Supports async views, WebSockets, Server-Sent Events,
#     and long-lived connections.
#   - Django generates asgi.py alongside wsgi.py since v3.0.
#   - Servers: uvicorn, daphne, hypercorn.
#
# Django default: WSGI
#   The development server (manage.py runserver) uses WSGI.
#
# When to switch to ASGI:
#   - You need WebSockets (e.g. real-time chat, live dashboards).
#   - You want to use async def views for non-blocking I/O.
#   - You are using Django Channels for event-driven features.
#   Switch by pointing your server at asgi.py instead of wsgi.py
#   and installing an ASGI server: pip install uvicorn
#   Then run: uvicorn coursemanager.asgi:application


# =============================================================
# STEP 4: MVC pattern → mapped to Django's MVT
# =============================================================
#
# MVC (Model-View-Controller) — the classic pattern:
#
#   Model      → represents data and business logic (DB layer)
#   View       → what the user sees (HTML, JSON output)
#   Controller → receives input, decides what to do, calls Model
#                and passes data to the View
#
# Django's MVT (Model-View-Template):
#
#   Model    ↔  Model      (same — ORM classes, DB interaction)
#   View     ↔  Controller (Django's View IS the controller —
#                           it handles the request, calls the
#                           model, and chooses a template)
#   Template ↔  View       (the HTML/JSON output the user sees)
#
# Mapping table:
#   MVC role        │ Django equivalent  │ Where it lives
#   ────────────────┼────────────────────┼─────────────────
#   Model           │ Model              │ courses/models.py
#   View (output)   │ Template           │ courses/templates/
#   Controller      │ View               │ courses/views.py
#
# The naming confusion: Django calls the "controller" a "View"
# because from Django's perspective, the View is what you
# write — it controls what data flows to the template.
# The Template is the actual presentation layer.
