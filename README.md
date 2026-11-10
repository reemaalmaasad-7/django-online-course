# OnlineCourse – Django Assessment Feature

A Django-based course application with models, admin inlines, Bootstrap templates, a course exam, submission tracking, and results evaluation.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations onlinecourse
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

On Windows use `.venv\Scripts\activate` instead of `source .venv/bin/activate`.

- Open `http://127.0.0.1:8000/admin/` to see the admin site.
- Local sample login: **demo_admin** / **DemoPass123!** (change this before any public deployment).
- Open `http://127.0.0.1:8000/` and click **Introduction to Django**.
- Answer all 3 questions with **Python**, **urls.py**, and **ORM**; submit to view **Congratulations** and detailed results.

## Screenshots for assessment

1. Capture the real admin interface as `03-admin-site.png` showing Authentication and Authorization and OnlineCourse.
2. Capture the real exam result as `07-final.png` showing Congratulations, score, and results.

## GitHub URLs required

Upload the project to a **public** GitHub repository. Use each file's actual `github.com/.../blob/main/...` URL:

1. `onlinecourse/models.py`
2. `onlinecourse/admin.py`
4. `onlinecourse/templates/onlinecourse/course_details_bootstrap.html`
5. `onlinecourse/views.py`
6. `onlinecourse/urls.py`

Tasks 3 and 7 require original screenshots of your running project, not links.

**Note:** This is an original starter implementation. Confirm it meets your course lab instructions and run it yourself before submitting. Do not deploy the included demo password or development SECRET_KEY to a public server.
