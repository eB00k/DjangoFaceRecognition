FROM python:3

ENV PYTHONBUFFERED=1

WORKDIR /code

COPY . /code

RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000  