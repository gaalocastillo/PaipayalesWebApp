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


#### API Endpoints

***Name:*** Get products

***Description:*** Get a list of the products available that belongs to a given category

***Method:*** GET

	```
	/api/v1/products/[category_name]
	```


***Name:*** User registration

***Description:*** Register a user by obtaining its information.

***Method:*** POST

	```
	/api/v1/auth/register
	```


***Name:*** User login

***Description:*** Allows the user to login by entering its credentials.

***Method:*** POST

	```
	/api/v1/auth/login
	```
