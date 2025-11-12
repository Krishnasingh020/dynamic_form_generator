This project is a Dynamic Form Generator built using Django.
The main idea was to create a system where I can build forms dynamically from the database instead of hardcoding them in HTML or Python.

Basically, I can define forms and their fields (like text, number, email, checkbox, etc.) in the backend, and Django will automatically generate and render the form on the frontend.

## what it does ?
Allows creating multiple forms dynamically.

Each form can have any number of fields.

Supports basic field types: text, number, email, checkbox, and select.

Renders the form dynamically at runtime using Django’s form system.

Handles validation automatically using Django’s form fields.

Can be extended easily to support more field types or save user responses.

## Technologies used

Backend: Django (Python)

Database: SQLite (default)

Frontend: HTML, Django Templates

## Run locally
```bash
git clone <repo-url>
cd django-dynamic-form-generator
 ```

```bash
python -m venv venv
source venv/bin/activate   
```

```bash
pip install -r requirements.txt
```
```bash
python manage.py makemigrations
python manage.py migrate
```
```bash
python manage.py runserver
```


