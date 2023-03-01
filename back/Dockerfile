FROM python:3.9


ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update
RUN apt-get install -y gdal-bin
RUN apt-get install -y vim
RUN apt-get install libatlas-base-dev

RUN pip install gunicorn
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .

CMD [ "gunicorn", "--config", "/code/gunicorn.conf.py", "djapp.wsgi:application"]

EXPOSE 8080
VOLUME /code
