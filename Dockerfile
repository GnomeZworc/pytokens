FROM python:3.6.6-stretch

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./app /app

WORKDIR /app

CMD python3 -u api.py
