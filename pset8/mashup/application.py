import os
import re
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue

from cs50 import SQL
from helpers import lookup

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")

@app.route("/")
def index():
    """Render map."""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))

@app.route("/articles")
def articles():
    """Look up articles for geo.
    In this section we respond to requests made through get method
    unlike the 'post' method of query in finance
    request can be made with postal code, place/country name
    """
    if request.method == "GET" :

        if not request.args.get("geo") :
            raise RuntimeError("missing geo")

        # get query value
        geo = request.args.get("geo")

        # get news for query
        news = lookup(geo)
        return jsonify(news)

@app.route("/search")
def search():
    """Search for places that match query.
    In this section we respond to requests made through get method
    unlike the 'post' method of query in finance
    request can be made with postal code, place/country name
    """

    if request.method == "GET" :

        # store search query
        q = '%' + request.args.get("q") + '%'

        # search in database for query

        try :
            places = db.execute("""SELECT * FROM places WHERE longitude LIKE :q OR postal_code LIKE :q OR
                                    latitude LIKE :q OR place_name LIKE :q OR admin_name1 LIKE :q OR
                                    admin_name2 LIKE :q OR admin_name3 LIKE :q;""", q=q)
            return jsonify(places)

        except :
            raise RuntimeError("error while search")

@app.route("/update")
def update():
    """Find up to 10 places within view."""

    # ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # explode southwest corner into two variables
    (sw_lat, sw_lng) = [float(s) for s in request.args.get("sw").split(",")]

    # explode northeast corner into two variables
    (ne_lat, ne_lng) = [float(s) for s in request.args.get("ne").split(",")]

    # find 10 cities within view, pseudorandomly chosen if more within view
    if (sw_lng <= ne_lng):

        # doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # output places as JSON
    return jsonify(rows)

# function name should be same as route name else error is generated
@app.route("/place")
def place() :
    """ get place name on marker click to get articles"""

    if not request.args.get("q"):
        raise RuntimeError("missing sw")
    if not request.args.get("r"):
        raise RuntimeError("missing nw")

    # round values to remove floating poin imprecision
    q = round(float(request.args.get("q")), 4)
    r = round(float(request.args.get("r")), 4)

    try :
        # place name
        rows = db.execute("SELECT place_name FROM places WHERE latitude LIKE ':ltd' AND longitude LIKE ':lng';", ltd=q, lng=r)
    except :
        raise RuntimeError("counld not find place name")

    # jsonify is required for acceptable return to callback function of json call
    # otherwise it'll result in an error
    # also, pass the output row to jsonify else string will not be assigned to new variable
    return jsonify(rows)
