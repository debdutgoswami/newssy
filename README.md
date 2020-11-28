<p align="center">
    <img src="assets/favicon.png" width="300px" alt="Logo" >
    <h3 align="center">Newssy</h3>
    <br />
    <p align="center">
      One Stop News for all 📰
      <br />
      <br />
      Look through News from various sources and subscribe to newsletters to receive daily headlines via email
      <br />
      <br />
      <a href="https://github.com/debdutgoswami/newsfeed/issues/new?assignees=&labels=&template=bug_report_template.md&title=">Report Bug</a>
      ·
      <a href="https://github.com/debdutgoswami/newsfeed/issues/new?assignees=&labels=&template=feature_request_template.md&title=">Request Feature</a>
    </p>
</p>

---

## Contributing

1. All PRs should be merged to `development` branch. So always change to `development` branch.

---

## Development

1. Clone the repository

2. Download `redis` for `email queue`

3. Create a `virtual environment` for python inside `app/api`

4. Change directory to `app/` and activate the `venv` and install all modules from `requirements.txt` using `pip`

5. Then run `redis server`.

6. Create a `start_api.sh` script which will export all the `environment variables` and will run the flask app and also `Celery`. To know how to run `Celery`, again refer to the [link](https://pratos.github.io/2017-01-12/celery-setup-on-windows/) provided in the previous step.


### Setting up PostgreSQL for development

1. Install postgresql

2. Start the service by typing `service postgresql start`

3. (optional) To connect to the database via CLI, type, `sudo -u <username> psql`. The default username is `postgres`

    To connect to database, type `\c <databasename>` in psql CLI. Here, the name is `newsfeed`.

    Type `\dt` to list the tables inside the database.

    Type `select * from <tablename>` to show the entire content of the database.

### Setting up Redis for development

1. Install redis server

2. Start the service by typing `service redis-server start`

3. (optional) Connect to redis via redis-cli, type `redis-cli` then type `ping` in the cli

---

Deployment (Google Cloud Platform)
======

### Setting CloudSQL

We will be using a postgresql. Follow this [documentation](https://cloud.google.com/sql/docs/postgres/connect-external-app#sqlalchemy-unix).

1. Create a service account key (JSON)

2. Download `cloud_sql_proxy` and make it executable using `chmod +x cloud_sql_proxy`

3. Create a user in the database and add an appropiate password

4. Create a database named `newsfeed`

5. Database URI should be of the following format <pre>postgresql+psycopg2://{username}:{password}@/?host=/cloudsql/{connection_name}</pre>

6. Run the proxy first. Type the following to run it. 
    <pre>./cloud_sql_proxy -dir=/cloudsql -instances={connection_name} \
                -credential_file={service_account_key} &</pre>

7. Now, create the tables. To create the tables, simply export the environment variables and then type the following in your terminal. <pre>python manage.py create_db</pre>

### Production

Simply create `env`, `key`, `certs` folder. Add all the `.env` files inside `env` folder, add the `service account key` to `key` folder and add the certificates to the `certs` folder. The last one is optional (if you want ssl certificate). 

Make a folder inside `docker` called `cloudsql` and give it read and write permission using chmod. Also create a `.env` file which will contain the database's connection name. Don't forget to create a database in `Cloud SQL`

Go inside `docker` folder and simply run `./run_docker.sh` and your server should be up and running. Don't forget to change your servers firewall settings to allow `http` and `https` connections.

### Creating SSL certificate with letsencrypt (last step)

To install letsencrypt vertificates with docker-compose, you need to use the letsencrypt docker image. Follow this [guide](https://www.humankode.com/ssl/how-to-set-up-free-ssl-certificates-from-lets-encrypt-using-docker-and-nginx) to get started.
