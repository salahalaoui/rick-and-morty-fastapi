# Rick-and-morty app

## Deploy using Docker

To deploy this project using docker :

```bash
$ git clone https://github.com/salahalaoui/rick-and-morty-fastapi
```

Now move to the project root directory. The `.env` is committed to git history
just for the convenience of the developer reading this code: sensible environment variables should never be published in repositories.

```bash
$ mv rick-and-morty-fastapi
$ docker compose build
$ docker compose up
```

The API implements some routes that should not stay unprotected. In order to use these routes you should first authenticate at the top right of the application docs (`0.0.0.0:8080/docs`) in the button that reads `Authorize`. Before that you need to create a new user with the POST `register`

## Migration from json to pricemap

In the app container to migrate data from previous json files to the postgres database :

```bash
$ docker exec -it app bash
$ python3 migration_from_json.py
```

## Authentification

The API uses Bearer token from `OAuth2PasswordBearer` instead of a static api key, it's more secure because even it's compromised the token will expire and the user will have to ask for a new token.

## Stack

The docker-compose.yml is configured to create :

- an image of the application named `app`,
- an image of PostgreSQL where we only store the user,
- an image of RabbitMQ –`rabbit`– as celery broker
- an image of Redis v6.2 –`redis` for celery backend
- an image of flower to monitor celery tasks at `localhost:5556`.
- an image of pgadmin for PostgreSQL database administration at `localhost:5050`

To see the application working sound and safe, please visit the URI `localhost:8080/docs`

Instead of using `psycopg2` directly to connect to the postgreSQL database, the api uses SQLAlchemy, an object-relational mapper, we don't need to do sql queries in the python code; instead SQLAlchemy allows to manipulate python objects, which is way more simpler, also, we don't have to deal with the specificity of a database type. SQLAlchemy is an abstraction layer.

The application uses Alembic. Alembic is great for easily making changes to database models.

## Backlog

- For fetching meta data from imbd I will use `Beautifulsoup` , which is an excellent library for scrapping html data `https://www.crummy.com/software/BeautifulSoup/bs4/doc/`
- Implementation of a comment moderation workflow: : For this I think the best is to create a Role table, each user has a role (admin, user, moderator). We can then authorize certain routes according to the role of the user, whether it is a superuser or a normal user.

The comment table would have an additional status column (`new`, `in review`, `rejected`, `approved`), we must also add a `GET /review_comments` route so that moderators can access the comments to be validated, we already have a `PATCH /comments` route for edit the comment.

In addition to this, the `GET /comments` route must be modified to filter only on comments already approved,

- Statistical indicators (in csv format) : Thanks to sqlalchemy we have access to high-level relationships to easily obtain the comments linked to an episode, we can easily obtain the count or filter before on the status of the comments or the average length of the body of the comments

I added `celery` in the application, I think for future development especially those of the current backlog `celery` can bring a real advantage. For example `celery` allows to have a periodic task which will run once a day for example at 3am to get the comments of the last 24 hours, process them and make them available in file format, then the PO can simply get the file which will subsequently be a huge time saver.
