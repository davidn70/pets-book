import os
import json
import requests
from flask import Flask, make_response, render_template, request, redirect
#import firebase_admin
#from firebase_admin import credentials
#from firebase_admin import firestore
import google.cloud
from google.cloud import storage, vision
#from wand.image import Image

#PREFIX = "thumbnail"
#client = storage.Client()
vision_client = vision.ImageAnnotatorClient()

app = Flask(__name__)

def root_dir():
    """ Returns root director for this project """
    return os.path.dirname(os.path.realpath(__file__ + '/..'))


def nice_json(arg):
    response = make_response(json.dumps(arg, sort_keys = True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response


@app.route("/", methods=['GET'])
def main():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "thumbnail": "/makethumbnail",
            "checkimage": "/checkimage/<username>"
        }
    })


@app.route("/makethumbnail", methods=['GET', 'POST'])
def make_thumbnail(data, context):

    # don't do this with thumbnails generated by this function
    if data['name'].startswith(PREFIX):
        return

    newName = f"{PREFIX}-{data['name']}"
    # this is the id of the item in firestore - image name without .jpg
    oldName = data['name'][:-4]
    size = 280

    # Get the bucket which the image has been uploaded to
    bucket = client.get_bucket(data['bucket'])
    # get the image
    thumbnail = Image(blob=bucket.get_blob(data['name']).download_as_string())

    # only resize if it's bigger than our maximum size
    if size < thumbnail.width:
        print('resizing image ' + oldName)
        newHeight = int((size * thumbnail.height) / thumbnail.width)
        thumbnail.resize(size, newHeight)
    
    # resized or not, this is theo ne we need to check for inappropriate content
    thumbnail_blob = bucket.blob(newName)

    safe = check_image(data)

    if safe:
        thumbnail_blob.upload_from_string(thumbnail.make_blob())
    else:
        print('Replacing inappropriate image with default No Image jpg')
        replacement = Image(blob=bucket.get_blob('NoImage.jpg').download_as_string()) 
        thumbnail_blob.upload_from_string(replacement.make_blob())  

    # make the approved thumbnail public
    thumbnail_blob.make_public()  

    print('updating firestore document with name of approved image')
    happenings = firestore.Client().collection('happenings')
    doc = happenings.document(oldName).get().to_dict()
    doc['image'] = newName[:-4]
    happenings.document(oldName).set(doc)

@app.route("/checkimage", methods=['GET', 'POST'])
def check_image():
    if request.method == 'GET':
        print("This was a GET")
        return("This was a GET")

    if request.method == 'POST':
        print("This was a POST")
        file_name = request.form['name']
        print(f'file_name {file_name}')
        bucket_name = request.form['bucket']
        print(f'bucket_name {bucket_name}')
        #file_name = str(uuid.uuid4())
        #print(f'file_name is now {file_name}')

        blob_uri = f'gs://{bucket_name}/{file_name}'
        print(f'blob_uri {blob_uri}')
        blob_source = {'source': {'image_uri': blob_uri}}
        print(f'blob_source {blob_source}')

        print(f'Analyzing {file_name} in vision API.')

        result = vision_client.safe_search_detection(blob_source)
        detected = result.safe_search_annotation

        if detected.adult == 5 or detected.violence == 5:
            print(f'The image {file_name} was detected as inappropriate.')
            return "false"
        else:
            print(f'The image {file_name} was detected as OK.')
            return "true"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


