from flask import Flask, request, jsonify
import json

class Base:
    app = Flask(__name__)

    @staticmethod
    def asJSON(data):
        from config import Config
        if Config.JSONfile is True:
            return jsonify(data)
        else:
            return json.dumps(data)
