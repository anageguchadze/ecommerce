Django E-Commerce API with CI/CD

This project is a Django-based REST API for an e-commerce platform that includes functionality for managing products, orders, and order items. The API includes features like authentication, CRUD operations, and integrates with a PostgreSQL database. The repository also includes a CI/CD pipeline using GitHub Actions to automate testing and deployment.

Key Features:
Product Management: Add, update, delete, and list products.
Order Management: Create, list, and retrieve orders with order items.
Authentication: Token-based authentication using Django REST framework.
CI/CD Pipeline: Automated testing and database migrations with GitHub Actions.
Database Integration: Uses PostgreSQL for storing data.

Installation and Setup
1. Clone the repository
Clone the repository to your local machine:
git clone https://github.com/anageguchadze/ecommerce.git

2. Create a virtual environment
Create a virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows

4. Install dependencies
Install the required Python dependencies:
pip install -r requirements.txt

6. Set up the database
Make sure you have PostgreSQL running. You can use the local PostgreSQL instance or Docker to spin up a container with the PostgreSQL service.

For local setup, update the DATABASE_URL in settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

Run the migrations to set up the database:
python manage.py migrate

5. Create a superuser (Optional)
To access the Django admin panel, you can create a superuser:
python manage.py createsuperuser

7. Run the server
Run the development server:
python manage.py runserver
Your API will be accessible at http://127.0.0.1:8000/.

API Endpoints
Product Endpoints
GET /products/ - List all products
POST /products/ - Create a new product
GET /products/{id}/ - Retrieve a single product
PUT/PATCH /products/{id}/ - Update a product
DELETE /products/{id}/ - Delete a product
Order Endpoints
GET /orders/ - List all orders
POST /orders/ - Create a new order
GET /orders/{id}/ - Retrieve an order
Authentication
POST /login/ - Obtain an authentication token
Testing

Run the test suite to ensure everything is working correctly:
python manage.py test
CI/CD Pipeline with GitHub Actions
This project includes a CI/CD pipeline set up using GitHub Actions to run automated tests and deploy the application to the server. The pipeline is triggered on every push to the main branch and for pull requests to the main branch.

Workflow Steps:
Checkout the code.
Set up Python: Install the required Python version.
Install dependencies: Install project dependencies from requirements.txt.
Run migrations: Apply database migrations.
Run tests: Run unit tests to verify the code is correct.

Contributing
Feel free to fork this project, create an issue, and submit pull requests. Contributions are always welcome!

License
This project is licensed under the MIT License - see the LICENSE file for details.

