mysql --default-character-set=utf8 -u root project < create_database.sql

pushd ..
rm -rf ./project/migrations/0*.py
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
popd

mysql --default-character-set=utf8 -u root project < testdata.sql

echo ""
echo "--------------------------"
echo "--- Test data imported ---"
echo "--------------------------"
echo ""