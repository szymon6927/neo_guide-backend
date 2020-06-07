# neo_guide-backend

Project description

## Stack

- ...

## Development

1. ...

## Dependencies

Update dependencies and format code using Makefile:

```
make update-deps
make format
```

## Pre-commit config

We use a pre-commit hook which checking a quality of code. To install a hook on your local repository, you have to run a command given below, after install required packages:

```
pre-commit install
```

## Documentation

Documentation available under url `/docs` or `/swagger`

## Unit tests

To run tests run:

```
pytest neo_guide
```

### Load testing
The `/neo_guide/load_tests` directory contains a definitions of load tests.
It's required to declared a few envs for correctly tests execution:
```bash
LOCUST_USER_EMAIL=
LOCUST_USER_PASSWORD=
LOCUST_HOST=  # eg. http://127.0.0.1:8000/
```

Then in project root type:
```
$ locust -f neo_guide/load_tests/locustfile.py
```

then open a locust web UI:
```
http://localhost:8089/
```
