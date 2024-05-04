# waltz

Quick boilerplate for Django.

## Installation

Install Python via tool like pyenv or rye. Then, install uv.

Create a new virtual environment using uv:

```bash
uv venv
```

Install all dependencies:

```bash
uv pip install -r requirements/dev.txt
```

Setup .env file:

```
# Django
DJANGO_SETTINGS_MODULE=src.config.settings.dev
# Postgres
POSTGRES_DB=waltz
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
```

Build Docker images:

```bash
make build
```

Start Docker containers:

```bash
make up
```

## Testing production setup

Testing the production Docker setup is a little tricky with Docker Compose.
This is because Docker Compose volume will override the permissions of the app
folder. Also, you need a proxy on top of Gunicorn to serve the static files.
Here is a quick tutorial to set things up locally.

Remove target and set user to root:

```yml
&default-app
    build:
      dockerfile: ./Dockerfile
    user: root:root
```

Thanks to that, volume will not mess up the permissions. You can trust me, the
nonroot user will work in the normal setup.

Then replace 'ports' with 'expose':

```yml
services:
  django:
    <<: *default-app
    expose:
      - 8000:8000
```

Add '.nginx.conf' file:

```
events {
	worker_connections 1024;
}

http {
	types {
		text/css    css;
		text/html   html;
		application/javascript   js;
	}

	upstream waltz {
		server django:8000;
	}

	server {
		listen 8080;

		location / {
			proxy_pass http://waltz;
			proxy_set_header Host $host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header X-Forwarded-Proto $scheme;
			proxy_redirect off;
		}

		location /static/ {
			alias /code/src/.static/;
		}
	}
}
```

Add nginx image to Docker Compose config:

```yml
nginx:
    image: nginx:latest
    volumes:
      - ./.nginx.conf:/etc/nginx/nginx.conf
      - staticfiles:/code/src/.static
    ports:
      - 8080:8080
```

You will need the same 'staticfiles' volume in the Django section.

Rebuild the Django image and run everything with `make up`. You can now look
for the app on 'localhost:8080'.

## Batteries

- Users + JWT
- Swagger
- Logging
- Celery + Beat
- Redis cache
- RabbitMQ broker
