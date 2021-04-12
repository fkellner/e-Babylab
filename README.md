# e-Babylab
e-Babylab is an open source authoring tool that allows users or researchers to easily create, host, run, and manage online experiments, without writing a single line of code. Using this tool, experiments can be programmed to include any combinations of image, audio, and/or video contents as stimuli and record key presses, clicks, screen touches, audio, and video.

## Contents
1. [Installation](#1-installation)
2. [Executing Django Commands](#2-executing-django-commands)
3. [Upgrade](#3-upgrade)
4. [Troubleshooting](#4-troubleshooting)
5. [Useful Links](#5-useful-links)

## 1. Installation

### Requirements
e-Babylab runs in a containerized environment using Docker and Docker Compose. No other software is required.

To install Docker, please follow the instructions below:
* **Linux:** [Docker](https://docs.docker.com/engine/installation/), [Docker Compose](https://docs.docker.com/compose/install/)
* **Windows:** [Docker for Windows](https://docs.docker.com/docker-for-windows/install/) (includes Docker Compose)
* **Mac:** [Docker for Mac](https://docs.docker.com/docker-for-mac/install/) (includes Docker Compose)

For development, we recommend you to study the [Docker](https://docs.docker.com/get-started/) and [Docker Compose](https://docs.docker.com/compose/gettingstarted/) documentation.

### Run Local Development Environment
For local development, you can run a development version of e-Babylab using the following command:

```bash
docker-compose -f docker-compose.dev.yml up -d
```

The development environment additionally installs pgadmin for easy access to the database. It will be accessible via a random
port on your system. You can use `docker ps -a` to find out about the port. pgadmin is then at `http://localhost:PORT/login`.
You can find the credentials for pgadmin in the `docker-compose.dev.yml` file.

If you are running e-Babylab for the first time, you will need to:

1. Set up the database using `docker-compose -f docker-compose.dev.yml exec web python manage.py migrate`. 
2. Expose new static files (e.g., JavaScript files) using `docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic`.
3. Create a superuser (for logging into the admin interface) using `docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser`.

Once everything is set up, Django admin can be accessed at `http://localhost:8080/admin/`.

If you have made any changes to the data models during development, you will need to create migration files and apply these afterwards. Migration files can be created using `docker-compose exec -f docker-compose.dev.yml web python manage.py makemigrations` and applied using `docker-compose exec -f docker-compose.dev.yml web python manage.py migrate`. For more information about migrations, please refer to the [Django documentation](https://docs.djangoproject.com/en/3.1/topics/migrations/).

e-Babylab can be stopped using `Ctrl + C` or `docker-compose -f docker-compose.dev.yml down`. 
To stop e-Babylab without destroying the containers, use `docker-compose -f docker-compose.dev.yml stop`.
For more information about their differences, please refer to the documentation for [docker-compose down](https://docs.docker.com/compose/reference/down/) and [docker-compose stop](https://docs.docker.com/compose/reference/stop/).

### Run in Production
The production environment of e-Babylab additionally uses nginx for HTTPS/TLS support. You will need to:

1. Create `docker-compose.yml` by copying `docker-compose.yml.template` and add valid TLS certificates to the nginx container via volumes in `docker-compose.yml`.
2. Create `nginx.conf` by copying `nginx.conf.template` and replace `<your_domain.com>` with your actual domain.

By default, the TLS certificates are expected to be at the following locations:

* `/etc/ssl/certs/cert.pem`
* `/etc/ssl/private/server.key`

The locations can be customized in the nginx config `nginx.conf`.

Use the following command to start:

```bash
docker-compose up -d
```

After starting, Django admin will be available at `https://<your_domain.com>:8443/admin`. 

As mentioned before, if you are running e-Babylab for the first time, you will need to:

1. Set up the database using `docker-compose exec web python manage.py migrate`. 
2. Expose new static files (e.g., JavaScript files) using `docker-compose exec web python manage.py collectstatic`.
3. Create a superuser (for logging into the admin interface) using `docker-compose exec web python manage.py createsuperuser`.

## 2. Executing Django Commands
You can use the following commands to execute commands inside the Django container:

```bash
docker-compose exec web django-admin <command> [options]
docker-compose exec web python manage.py <command> [options]
```

These can be used, for example, to perform upgrades or to create superusers. All available commands can be found [here](https://docs.djangoproject.com/en/3.1/ref/django-admin/).

## 3. Upgrade
To upgrade an existing environment to the latest version of e-Babylab, please run the following steps:

1. We recommend installing e-Babylab from either a public or private git repository, to persist your settings. 
    To pull the latest changes from the repository, please run `git pull`.
2. To upgrade, we first need to recreate all containers, so that they are using the latest version of e-Babylab.

    First shutdown the environment using `docker-compose down`. This will remove all containers, but retain the volumes which contain all of your data.

    Next run `docker-compose build` to force a rebuild of the e-Babylab container.

    Finally you can restart the environment using `docker-compose up -d`.
3. Next you need to perform the database migration. You can apply all migrations using `docker-compose exec web python manage.py migrate`.
4. To expose new static files (e.g., JavaScript files), run `docker-compose exec web python manage.py collectstatic`.

## 4. Troubleshooting

### Web Container starts with `"exec: \"./wait-for-it.sh\": permission denied"`
Allow the execution of the *wait-for-it.sh* script by executing the following command:
`chmod +x ipl/wait-for-it.sh`

### `"Server error (500)"` when attempting to download results
Make sure that there is a "webcam" directory in the "ipl" directory (where manage.py and the Dockerfile are located). If it does not exist, create one. 

### `"Can't find a suitable configuration file in this directory or any parent. Are you in the right directory?"`
Docker is unable to locate `docker-compose.yml`. Either create this file (by copying `docker-compose.yml.template`) or run `docker-compose` commands with `-f docker-compose.dev.yml` (e.g., `docker-compose -f docker-compose.dev.yml build`). 

## 5. Useful Links
* [e-Babylab User Manual](https://github.com/lochhh/e-Babylab/wiki)
* [HandBrake](https://handbrake.fr/) (for resizing video files and converting .webm to other formats) 
* [Django Tutorial](https://docs.djangoproject.com/en/3.1/intro/overview/)
* [Django with Docker](https://docs.docker.com/compose/django/)

This software is licensed under the [Apache 2 License](https://www.apache.org/licenses/LICENSE-2.0).
