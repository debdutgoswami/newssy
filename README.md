# Newsfeed

---

## Contributing

1. Check [CODE OF CONDUCT](https://github.com/debdutgoswami/newsfeed/blob/master/CODE_OF_CONDUCT.md) to know how to setup your `development` enviornment.

2. All PRs should be merged to `development` branch. So always change to `development` branch.

---

## Development

1. Clone the repository

2. Download `RabbitMQ` for `email queue`

3. Create a `virtual environment` for python inside `app/api`

4. Change directory to `app/` and activate the `venv` and install all modules from `requirements.txt` using `pip`

5. The run `RabbitMQ Server`. Go to this [link](https://pratos.github.io/2017-01-12/celery-setup-on-windows/) to get a detailed guide.

6. Create a `start_api.sh` script which will export all the `environment variables` and will run the flask app and also `Celery`. To know how to run `Celery`, again refer to the [link](https://pratos.github.io/2017-01-12/celery-setup-on-windows/) provided in the previous step.

---