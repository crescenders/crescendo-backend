rm -rf migrations
rm db.sqlite
flask db init
flask db migrate
flask db upgrade