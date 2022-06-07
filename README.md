# README

## setup
```shell
docker-compose build
docker-compose run web python manage.py migrate
docker-compose run web python manage.py load_data
docker-compose up -d
```

## running tests

```shell
docker-compose run web python manage.py test api.tests
```