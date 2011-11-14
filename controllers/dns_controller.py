from base import app, asJSON

class DNSController:
    @app.route("/dns/list", methods=['GET', 'POST'])
    def list():
        data = {}
        return asJSON(data)
        
    @app.route("/dns/save", methods=['GET', 'POST'])
    def save():
        data = {}
        return asJSON(data)
        
    @app.route("/dns/get", methods=['GET', 'POST'])
    def get():
        data = {}
        return asJSON(data)
        
    @app.route("/dns/delete", methods=['GET', 'POST'])
    def delete():
        data = {}
        return asJSON(data)