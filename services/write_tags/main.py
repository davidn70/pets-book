from flask import Flask
from google.cloud import bigquery


app = Flask(__name__)


@app.route("/", methods=['GET'])
def main():
    return "try doing a GET on /tag/pet_id/label"


# SELECT DISTINCT pet_id FROM `still-bank-234915.Pets.pet_labels` WHERE
# REGEXP_CONTAINS(label, '') LIMIT 20
@app.route("/tag/<pet_id>/<label>", methods=['GET'])
def user_suggested(pet_id, label):
    bigquery_client = bigquery.Client()
    dataset = bigquery_client.dataset('Pets')
    left = bigquery.SchemaField('pet_id', 'STRING', 'REQUIRED')
    right = bigquery.SchemaField('label', 'STRING', 'REQUIRED')
    table = dataset.table('pet_labels')
    ROWS_TO_INSERT = []
    row = {}
    row["pet_id"] = pet_id
    row["label"] = label
    ROWS_TO_INSERT.append(row)
    bigquery_client.insert_rows(table, ROWS_TO_INSERT,
                                selected_fields=[left, right])
    return "OK"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
