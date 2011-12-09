from base import app, asJSON, Messages
from service.dnshandler import DNSHandler
from flask import request

class DNSController:
    @app.route("/dns/list", methods=['GET', 'POST'])
    def list():
        data = {}
        dns = DNSHandler()
        data["zones"] = dns.getAllEntries()
        if len(data["zones"]) > 0:
            data["success"] = True
        return asJSON(data)
        
    @app.route("/dns/add", methods=['GET', 'POST'])
    def add():
        data = {}
        msgs = Messages()
        ip = request.args.get('ip')
        if not ip:
            msgs.add(u"no ip address supplied")
        name = request.args.get('name')
        if not name:
            msgs.add(u"no name supplied")
        if not len(msgs.getAll()) > 0:
            dns = DNSHandler()
            data = dns.add(ip, name)
        else:
            data["errors"] = msgs
        if data.has_key("error") or data.has_key("errors"):
            data["success"] = False
        return asJSON(data)
        
    @app.route("/dns/editName", methods=['GET', 'POST'])
    def editName():
        data = {}
        msgs = Messages()
        ip = request.args.get('ip')
        if not ip:
            msgs.add(u"no ip address supplied")
        name = request.args.get('name')
        if not name:
            msgs.add(u"no name supplied")
        if not len(msgs.getAll()) > 0:
            dns = DNSHandler()
            data = dns.editName(name, ip)
        else:
            data["errors"] = msgs
        if data.has_key("error") or data.has_key("errors"):
            data["success"] = False
        return asJSON(data)
        
    @app.route("/dns/editIp", methods=['GET', 'POST'])
    def editIp():
        data = {}
        msgs = Messages()
        ip = request.args.get('ip')
        if not ip:
            msgs.add(u"no ip address supplied")
        name = request.args.get('name')
        if not name:
            msgs.add(u"no name supplied")
        if not len(msgs.getAll()) > 0:
            dns = DNSHandler()
            data = dns.editIp(name, ip)
        else:
            data["errors"] = msgs
        if data.has_key("error") or data.has_key("errors"):
            data["success"] = False
        return asJSON(data)
        
    @app.route("/dns/save", methods=['GET', 'POST'])
    def save():
        data = {}
        return asJSON(data)
        
    @app.route("/dns/get", methods=['GET', 'POST'])
    def get():
        data = {}
        dns = DNSHandler()
        return asJSON(data)
        
    @app.route("/dns/delete", methods=['GET', 'POST'])
    def delete():
        data = {}
        msgs = Messages()
        name = request.args.get('name')
        if not name:
            msgs.add(u"no name supplied")
        if not len(msgs.getAll()) > 0:
            dns = DNSHandler()
            data = dns.delete(name)
        else:
            data["errors"] = msgs
        if data.has_key("error") or data.has_key("errors"):
            data["success"] = False
        return asJSON(data)