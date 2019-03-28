from google.cloud import datastore
from google.cloud import bigquery
import datetime
import requests

import main

datastore_client = datastore.Client(main.PROJECT)
API_ENDPOINT = "http://35.188.88.210:8080/checkimage"


def get():
    query = datastore_client.query(kind='Pet')
    query.order = ['-likes']
    pets = list(query.fetch())
    return pets


def like(pet_id):
    key = datastore_client.key("Pet", pet_id)
    pet = datastore_client.get(key)

    if("likes" in pet):
        pet['likes'] += 1
    else:
        pet['likes'] = 1

    print("{} has been liked {} times.".format(pet['petname'], pet['likes']))
    datastore_client.put(pet)
    return pet


def search(search_term):
    bigquery_client = bigquery.Client()

    query_params = [bigquery.ScalarQueryParameter('search_term', 'STRING', search_term.lower())]
    job_config = bigquery.QueryJobConfig()
    job_config.query_parameters = query_params

    query_job = bigquery_client.query("""SELECT DISTINCT pet_id FROM `still-bank-234915.Pets.pet_labels` WHERE REGEXP_CONTAINS(label, @search_term) LIMIT 20 """,
    location='US', job_config=job_config)

    results = query_job.result() 
    keys = []
    for row in results:
        key = datastore_client.key("Pet", row.pet_id)
        keys.append(key)

    pets = datastore_client.get_multi(keys)
    return pets


def call_vision(bucket, name):
    # data to be sent to api
    data = {'bucket': bucket,
            'name': name}

    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=data)

    # extracting response text
    print(r.text)


def save(data, image_name):
    print(data)
    kind = 'Pet'
    id = image_name
    key = datastore_client.key(kind, id)
    pet = datastore.Entity(key=key)

    pet['added'] = datetime.datetime.now()
    pet['image'] = 'https://storage.googleapis.com/{}/{}.jpg'.format(main.BUCKET, image_name) 
    pet['likes'] = 0
    for prop, val in data.items():
        pet[prop] = val

    datastore_client.put(pet)

    bigquery_client = bigquery.Client()
    dataset = bigquery_client.dataset('Pets')
    left = bigquery.SchemaField('pet_id', 'STRING', 'REQUIRED')
    right = bigquery.SchemaField('label', 'STRING', 'REQUIRED')
    table = dataset.table('pet_labels')
    ROWS_TO_INSERT = []
    row = {}
    row["pet_id"] = id
    row["label"] = data["caption"].lower()
    ROWS_TO_INSERT.append(row)
    row = {}
    row["pet_id"] = id
    row["label"] = data["petname"].lower()
    ROWS_TO_INSERT.append(row)
    bigquery_client.insert_rows(table, ROWS_TO_INSERT, selected_fields=[left, right])
    call_vision(main.BUCKET, image_name)
