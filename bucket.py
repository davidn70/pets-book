from google.cloud import storage
import main

storage_client = storage.Client(project=main.PROJECT)
bucket = storage_client.get_bucket(main.BUCKET)


def upload(file, name):

    try:
        blob = bucket.blob('{}.jpg'.format(name))
        blob.upload_from_string(file.read(), content_type=file.content_type)
        blob.make_public()
        return blob.public_url
    except Exception as err:
        raise err
