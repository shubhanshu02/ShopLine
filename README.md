# ShopLine

The Modern e-commerce For Small-Scale Businesses

### Setup Instructions

1. Add the `.env` file for the project to the root folder.
2. `pipenv shell`
3. `pipenv install`
4. `python manage.py migrate`

### Development Practices

1. Make your changes
2. If database models were changed, run `python manage.py makemigrations` to migrate the project.
3. Apply database migrations using `python manage.py migrate` if necessary.
4. Run `python manage.py runserver` to check if the changes work.
