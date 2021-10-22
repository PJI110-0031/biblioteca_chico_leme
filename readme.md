# biblioteca_chico_leme

## Setup

_* It's recommended that the development process be performed in a virtual environment ([venv](https://docs.python.org/3/library/venv.html))_

### Requirements

- Python 3
- [gettext binaries](https://docs.djangoproject.com/en/3.2/topics/i18n/translation/#gettext-on-windows) (if on Windows)

### TL;DR

```shell
pip install -r requirements.txt   # Download dependencies
python manage.py migrate          # Setup database
python manage.py compilemessages  # Compile messages translations
python manage.py createsuperuser  # Create an admin user (needed to access admin area)
python manage.py populate_db      # Fill database (about 20 min)
python manage.py runserver        # Start server
```
