This is a Django project that is run using the 
python manage.py runserver
command.
Currently it will only work with a local postgreSQL instance running on your local host, but I am going to trade that out with an Azure DB soon. 
Once we migrate to Azure I'll set up CI/CD for the project using Github Actions/ Azure DevOps. 
The main branch will have a basic stable set up features and I will merge branches with distinct features after the move to Azure, until then, I am hitting main directly.


RabbitMQ is being used as the message queue for the Celery Backend. 