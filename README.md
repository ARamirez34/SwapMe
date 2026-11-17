# SwapMe 🔁

A marketplace for trading clothes and items with other people. Post something you don't need, browse what others are offering, and send trade offers.

> 🚧 **Work in progress:** this is an early visual prototype. The core screens work, but it isn't finished or deployed.

---

## ✨ Features

- **Accounts:** sign up, log in and edit your profile
- **Listings:** post items with photos, descriptions and tags, then edit or delete them
- **Feed and Explore:** browse new listings and search what's out there
- **Stalls:** every user has a "stall" showing everything they've posted
- **Likes:** save listings you're interested in
- **Trade offers:** offer one of your items in exchange for someone else's, then accept or decline offers you receive

## 🧰 Built with

- Python + [Django](https://www.djangoproject.com/)
- SQLite
- Pillow for image uploads
- HTML/CSS templates

## 🚀 Run it locally

```bash
python -m venv venv
venv\Scripts\activate          # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000.

For anything beyond local testing, set `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=False` as environment variables.
