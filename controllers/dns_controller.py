from base import app, asJSON, Messages
from service.dnshandler import DNSHandler
from flask import request

class DNSController:
    @withPassword
    @app.route("/dns/list", methods=['GET', 'POST'])
    def list():
        data = {}
        dns = DNSHandler()
        data["zones"] = dns.getAllEntries()
        if len(data["zones"]) > 0:
            data["success"] = True
        return asJSON(data)
        
    @withPassword
    @app.route("/dns/add", methods=['GET', 'POST'])
    def add():
        data = {}
        msgs = Messages()
        host = request.args.get('host')
        if not host:
            msgs.add(u"no host address supplied")
        name = request.args.get('name')
        if not name:
            msgs.add(u"no name supplied")
        if not len(msgs.getAll()) > 0:
            dns = DNSHandler()
            data = dns.add(name, host)
        else:
            data["errors"] = msgs
        if data.has_key("error") or data.has_key("errors"):
            data["success"] = False
        return asJSON(data)
        
    @withPassword
    @app.route("/dns/editName", methods=['GET', 'POST'])
    def editName():
        data = {}
        msgs = Messages()
        fromName = request.args.get('from')
        if not fromName:
            msgs.add(u"no from name supplied")
        toName = request.args.get('to')
        if not toName:
            msgs.add(u"no name supplied")
        if not len(msgs.getAll()) > 0:
            dns = DNSHandler()
            data = dns.editName(fromName, toName)
        else:
            data["errors"] = msgs
        if data.has_key("error") or data.has_key("errors"):
            data["success"] = False
        return asJSON(data)
        
    @withPassword
    @app.route("/dns/editIp", methods=['GET', 'POST'])
    def editHost():
        data = {}
        msgs = Messages()
        host = request.args.get('host')
        if not host:
            msgs.add(u"no host address supplied")
        name = request.args.get('name')
        if not name:
            msgs.add(u"no name supplied")
        if not len(msgs.getAll()) > 0:
            dns = DNSHandler()
            data = dns.editHost(name, host)
        else:
            data["errors"] = msgs
        if data.has_key("error") or data.has_key("errors"):
            data["success"] = False
        return asJSON(data)
        
    @withPassword
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