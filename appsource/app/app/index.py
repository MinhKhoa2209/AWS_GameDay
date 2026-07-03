from flask import Flask
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
server_name = "test http server with default 200 response"
creator_name = "Jonny Doe"
creator_email = "jdoe@amazon.com"
success_message = "Demo task completed"
unicorns_message = "Unicorns Rock!"


def check_unicorn_health():
    pass


def check_unicorn_status():
    pass


def welcome():
    pass


@app.route("/")
def start_server():
    return {"200": unicorns_message}


@app.route("/status")
def status():
    return {"200": unicorns_message}


@app.route("/health")
def health():
    return {"200": unicorns_message}


@app.route("/welcome")
def welcome():
    return {"200": unicorns_message}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
