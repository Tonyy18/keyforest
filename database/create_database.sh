mysql -u root project < create_database.sql
cd ..
rm -rf ./project/migrations/0*.py
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
