# Email Parser Assignment

Made with [Python](https://www.python.org/) and [JavaScript](https://developer.mozilla.org/en-US/docs/Web/javascript) using frameworks and tools such as [Django](https://www.djangoproject.com/), [Django Rest Framework](https://www.django-rest-framework.org/), [React](https://reactjs.org/), [Webpack](https://webpack.js.org/), [Babel](https://babeljs.io/), [TailwindCSS](https://tailwindcss.com/), and svg icons from [Fontawesome](https://fontawesome.com/).

Containerized with [Docker](https://www.docker.com/) and [Docker-Compose](https://docs.docker.com/engine/reference/commandline/compose/)

Default to **localhost:8000**

For production change the **SECRET_KEY**

[Postman API file](./email_parser/test_assets/email_assessment.postman_collection.json) 

## Install & Build the frontend

```
    pip install -r requirements.txt
    cd ./email_parser/frontend
    npm i
    npm run build
```

## Run test (Django)

```
    python ./email_parser/manage.py test
```

## Run developer server

```
    python manage.py makemigrations api --settings=email_parser.settings_dev 
    python manage.py migrate --settings=email_parser.settings_dev 
    python manage.py runserver --settings=email_parser.settings_dev
```

## Docker

```
    docker-compose up -d
```
