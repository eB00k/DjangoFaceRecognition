FROM python:3

ENV PYTHONBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip3 install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000  