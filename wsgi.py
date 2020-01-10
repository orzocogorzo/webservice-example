import csv
import json

from werkzeug.wrappers import Response, Request
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple


class Server (object):

    def __init__ (self):

        # DATABASE
        self.db = list(csv.reader(open("DB.csv"), delimiter=",", quotechar='"'))
        headers = self.db.pop(0)
        self.fields = {headers[i]: i for i in range(len(headers))}

        # WEB SERVICE
        self.urls = Map([
            Rule("/", endpoint="root"),
            Rule("/query", endpoint="query"),
            Rule("/query/<sector>", endpoint="query"),
            Rule("/query/<sector>/<districte>", endpoint="query"),
            Rule("/query/<sector>/<districte>/<barri>", endpoint="query"),
            Rule("/distance", endpoint="distance"),
            Rule("/favicon.ico", endpoint="favicon")
        ])

    def __call__ (self, environ, start_response):
        request = Request(environ)
        endpoint, values = self.urls.bind_to_environ(environ).match()

        if getattr(self, "on_" + endpoint):
            res = getattr(self, "on_" + endpoint)(request, **values)
        else:
            res = Response(["Bad Request"], status="400 Bad Request")(environ, start_response)

        return res(environ, start_response)

    def on_root (self, request):
        with open("index.html") as html:
            content = [html.read()]
            return Response(content, status="200 OK", mimetype="text/html")

    def on_distance (self, request):
        lat = request.args["lat"]
        lng = request.args["lng"]
        subset = []
        for row in self.db:
            if self.mesure_distance(row, lat, lng) < 500:
                subset.append(row)

        return Response(["test"], status="200 OK")

    def on_query (self, request, sector=None, districte=None, barri=None):
        subset = None
        if not sector and not districte and not barri:
             subset = [
                {
                    field: row[index]
                    for field, index in self.fields.items()
                } for row in self.db
            ][:1000]
        else:
            subset = []
            for row in self.db:
                if not self.filter_row(row, {"sector": sector, "districte": districte, "barri": barri}):
                    continue
                # row = ["Comercial", "Pareos Mariluz", "Ciutat Vella", "El Gotic", 12232, 2135411]
                # {"sector": "Comercial", "nom": "Pareos Mariluz", ""}
                new_row = {}
                for field, index in self.fields.items():
                    new_row[field] = row[index]
                    subset.append(new_row)

        geojson = self.to_geojson(subset)

        return Response([json.dumps(geojson)], status="200 OK", mimetype="application/json")

    def mesure_distance (self, row, lat, lng):
       # filtre per distància entre coordenades (per fer)
       return 300

    def filter_row (self, row, conditions):
        valid = True
        for condition, value in conditions.items():
            if value:
                valid = valid and row[self.fields[condition]] == value
            # valid = valid and (row[self.fields[condition]] == value or value is None)

        return valid

    def to_geojson (self, data):
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": row,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            float(row["lng"]),
                            float(row["lat"])
                        ]
                    }
                } for row in data
            ]
        }

    def on_favicon (self, request):
        return Response(["favicon"], status="200 OK", mimetype="text/plain")


if __name__ == "__main__":
    server = Server()
    run_simple("127.0.0.1", 8080, server, use_debugger=True, use_reloader=True)
