@Echo off
set port=%1
call "venv/Scripts/activate"
python manage.py runserver %port%