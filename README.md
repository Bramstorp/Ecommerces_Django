# Ecommerces_Django
Python Ecommerces Website made with Django

--Basic Featuers--

-Add/show Products

-Products Category

-User / Customer

-Login / Register / Logout

-Admin only / customer only

-Order items in add to cart

--Setup--

All libaryes need it in the requirment.txt

--Running Script--

1: To run the website open a terminal and CD to the Ecommerces_Django folder (Desktop\Ecommerces_Django)

2: python manage.py createsuperuser to create a admin user to use as login for the /admin part

3: python manage.py runserver to run the webserver

4: go to the localhost website http://127.0.0.1:8000/admin

5: login to the admin part and go to groups and add 2 groups for the permission part to work create [admin] and [customer]

6: for the mail part to work go to settings.py in the djangowebserver folder and under the SMTP Configuration add in EMAIL_HOST_USER add you gmail and EMAIL_HOST_PASSWORD add gmail password

-- If you dont see any models in the /admin part then make a quick migrate to do that

    1: python manage.py makemigrations

    2 python manage.py migrate

    and that should fix the model problem
    


--TO BE DONE--

Discount code

Refund

Saving credit card information

Handling payments with Stripe

Guest User
