mysql --default-character-set=utf8 -u root project < create_database.sql

cd ..
rm -rf project/migrations/0*.py
call venv/Scripts/activate
call python manage.py makemigrations
call python manage.py migrate

cd database
mysql --default-character-set=utf8 -u root project < testdata.sql

echo ""
echo "--------------------------"
echo "--- Test data imported ---"
echo "--------------------------"
echo ""