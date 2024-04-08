# Prospero - Your Django Project

A project aimed at bringing together some different sources of data on board games, and presenting them in an interesting way. 

## Prerequisites

* Docker installed ([https://www.docker.com/](https://www.docker.com/))
* Docker Compose installed ([https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/))

## Dependencies

This project utilizes the following dependencies:

* **Django:** The core web framework ([https://docs.djangoproject.com/en/4.1/](https://docs.djangoproject.com/en/4.1/))
* **Celery (Optional):** A task queue for asynchronous processing ([https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html)) I use this mainly to shift processing of larger data pulls to the background. 

**Additional dependencies** may be listed here, depending on your project's requirements. 

## Environment Variables

This project utilizes environment variables to store sensitive information like database credentials, API keys, etc. You'll need to create a file named `.env` in the root of your project with the following format:

## Containers

Currently set up to use a PostgreSQL DB and RabbitMQ (as the message broker for celery)
