@Echo off
set port=%1
call "venv/Scripts/activate"
python manage.py runserver 0.0.0.0:%port%