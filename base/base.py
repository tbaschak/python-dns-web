from flask import Flask, request, jsonify
import json

class Base:
    app = Flask(__name__.split('.')[0])

    @staticmethod
    def asJSON(data):
        from config import Config
        if Config.JSONfile is True:
            return jsonify(data)
        else:
            return json.dumps(data)
        
class Log:
    @staticmethod
    def debug(*args):
        if len(args) == 2:
            Base.app.logger_name = args[1]
        Base.app.logger.debug(args[0])
        Base.app.logger_name = Base.__name__.split('.')[0]