from base import app, asJSON
class Index:
    @app.route("/", methods=['GET', 'POST'])
    def index():
        data = dict(
            title = "Python DNS HTTP Service",
        )
        return asJSON(data)
