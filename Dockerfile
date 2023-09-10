FROM python:3.9-slim

RUN apt-get clean && apt-get -y update

RUN apt-get -y install nginx python3-dev build-essential

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY src/. .

EXPOSE 5000
CMD [ "python", "app.py" ]