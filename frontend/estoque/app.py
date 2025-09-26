from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from web3 import Web3
import json
import logging
# APIs
from api_estoque import api_estoque


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

app.register_blueprint(api_estoque, url_prefix='/estoque')

@app.route("/")
def index():
    return "API principal OK"
CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)