FROM gcr.io/google_appengine/python

RUN mkdir /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app

RUN apt-get update && \
    apt-get install -y python-psycopg2 && \
    pip install --upgrade pip && pip install -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["main.py"]
