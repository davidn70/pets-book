FROM gcr.io/google_appengine/python

RUN mkdir app

WORKDIR app

COPY requirements.txt app

RUN apt-get update && \
    apt-get install -y python-psycopg2 && \
    pip install --upgrade pip && pip install -r requirements.txt

COPY . app

EXPOSE 8080

ENTRYPOINT ["python"]

CMD ["main.py"]
