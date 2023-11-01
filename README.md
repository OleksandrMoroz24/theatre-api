# Theatre DRF api project

Imagine you're creating an API for a theatre in your local city. The idea is to allow visitors of the Theatre to make Reservations online and choose needed seats, without going physically to the Theatre.

## DB structure:
![image](https://media.mate.academy/theatre_diagram_6b8017611a.png)

## Setting up the environment:
<hr>
Python3 must be already installed

Windows
```shell
git clone https://github.com/OleksandrMoroz24/theatre-api.git
cd restaurant_kitchen_service
python -m venv venv
.\\venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata test_data_theatre.json
python manage.py runserver
```

MacOS
```shell
git clone https://github.com/OleksandrMoroz24/theatre-api.git
cd restaurant_kitchen_service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata test_data_theatre.json
python manage.py runserver
```

## Test User:
<hr>
After load test data you can use test user
<br>
Login: testuser@test.ua
<br>
Password: bimbimbambam
<br>
Also you need to use api/user/token to get access token

## Features:
<hr>
<ul>
<li>JWT authenticated</li>
<li>Admin panel /admin/
<li>Documentation is located at /api/doc/swagger/</li>
<li>Managing tickets and reservations</li>
<li>Creating theatre halls</li>
<li>Adding actors, genres and plays</li>
</ul>

