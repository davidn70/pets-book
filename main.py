from flask import Flask, render_template, request, redirect
import uuid
import json




BUCKET = 'tangopetpics'
PROJECT  = 'still-bank-234915'

app = Flask(__name__)

import database
import bucket

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        pets = database.get()
        model = {"title": "Awesome Pet Photos", "header": "Photos", "pets": pets}
        print('Pets Home Page Requested!')

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        pets = database.search(data['search'])
        model = {"title": "Awesome Pet Photos", "header": "Some Pets!", "pets": pets}
        print('Search Requested: ' + data['search'])

    return render_template('index.html', model=model)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        model = {"title": " Awesome Pet Pictures", "header": "Add a Pet"}
        return render_template('add.html', model=model)

    if request.method == 'POST':
        try:
            data = request.form.to_dict(flat=True)
            file = request.files['image']
            name = str(uuid.uuid4())
            # Save the Pet Photo
            pic_url = bucket.upload(file, name)
            print('Pet photo saved:{}'.format(pic_url))
            database.save(data, name)
            print('Pet info saved:{}'.format(data))

            return redirect('/')
        except Exception as ex:
            print('An error occurred while saving a pet'.format(str(ex)))
            return redirect('/error/{}'.format(str(ex)))


@app.route("/api/like/<pet_id>")
def like(pet_id):
    print('Like added for {}'.format(pet_id))
    pet = database.like(pet_id)
    data = {}
    data['likes'] = pet['likes']
    data['pet_id'] = pet.key.name
    json_data = json.dumps(data)
    return json_data


@app.route("/error/<message>")
def error(message):
    model = {"title": "Awesome Pet Photos", "header": "An Error Occured!",  "message": message}	
    return render_template('error.html', model=model)


@app.route("/signin")
def signin():
    model = {"title": "Awesome Pet Photos", "header":"Sign In"}	
    return render_template('signin.html', model=model)


@app.route("/test")
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)