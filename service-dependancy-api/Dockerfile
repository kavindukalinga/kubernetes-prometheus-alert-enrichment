FROM python:3.10-alpine3.15

WORKDIR /app

COPY ./app/ /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python /app/alertmappingapi.py