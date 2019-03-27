from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def something():
    print("Hello world!")
    return("Hello world!")

@app.route("/wtf", methods=['GET', 'POST'])
def wtf():
    print("wtf")
    return("wtf")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
