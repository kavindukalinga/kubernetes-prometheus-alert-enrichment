FROM python:3.10-alpine3.15

WORKDIR /app

COPY getconnectionsdirectly.py /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python /app/getconnectionsdirectly.py