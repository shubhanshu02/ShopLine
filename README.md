# ShopLine

The Modern e-commerce For Small-Scale Businesses

### Update (As on 24th December 2020)

This project was presented on 24th December 2020 at 2:15 pm. The presentation can be found at this [link](https://www.canva.com/design/DAEOCZR5Fp0/8ZWqMjpepjejJgCOFVVT0g/view?utm_content=DAEOCZR5Fp0&utm_campaign=designshare&utm_medium=link&utm_source=sharebutton) and the website can be used using this [link](https://shopline-web.herokuapp.com/).
To report any issues, create an issue on this repository giving details of the problem.

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
