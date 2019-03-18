# Paipayales Web App
### A Django project for an online shop to manage the inventory.

#### How to run this project

1. Create Virtual Enviorment
	```
	virtualenv --python=`which python3` env
	```

2. Install dependencies
	```
	pip install -r requirements.txt
	```

3. Go To Project root `inventoryms/` and  Make migrations and migrate
	```
	./manage.py makemigrations && ./manage.py migrate
	```

4. Run the server
	```
	./manage.py runserver 0:9090
	```

