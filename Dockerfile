FROM python:3.12.1-slim  

WORKDIR /app  
RUN apt-get update && apt-get install -y build-essential 
COPY requirements.txt /app/ 
RUN pip install -r requirements.txt 

COPY . /app  

EXPOSE 8000  

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
