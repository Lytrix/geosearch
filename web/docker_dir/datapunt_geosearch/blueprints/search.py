# Python
import json
# Packages
from flask import Blueprint, request, jsonify, current_app
# Project
from datapunt_geosearch.datasource import AtlasDataSource
from datapunt_geosearch.datasource import NapMeetboutenDataSource
from datapunt_geosearch.elastic import Elastic

search = Blueprint('search', __name__)
es = Elastic()


#@search.route('/search', methods=['GET'])
def search_list():
    """List search endpoints"""
    # @TODO can it be automated?
    return json.dumps({
        '/search/geosearch_radius': 'Search in a radius around a point',
        '/search/geosearch_area': 'Search within a given area'
    })

search.route('/', methods=['GET'])
def help():
    """Help text en query index"""
    return json.dumps({
        '/nap': 'Search in a radius around a point in nap',
        '/atlas': 'Search in a radius around a point in atlas'
    })

    #@search.route('/search/geosearch_radius', methods=['GET', 'POST'])
def search_radius():
    """Performing a geo search for radius around a point"""
    resp = None
    # Making sure point and radius are given
    radius = request.args.get("radius")
    if not radius:
        resp = {"error": "Radius not found in get parameters"}
    # Checking either coords arra yor lat en lon
    coords = request.args.get('coords')
    if not coords:
        lon = request.args.get('lon')
        lat = request.args.get('lat')
        if not lat or not lon:
            resp = {"error": "No coordinates found"}
        coords = [lon, lat]
    # @TODO add support for filter and exclude
    # If no error is found, query
    if not resp:
        resp = es.search_radius(coords, radius)
    return json.dumps(resp)


#@search.route('/search/geosearch_area', methods=['GET', 'POST'])
def search_area():
    """Perform geo search in an area"""
    resp = {}
    limits = {}
    area_limits = ('top', 'left', 'bottom', 'right')
    for limit in area_limits:
        arg = request.args.get(limit)
        if not arg:
            resp['missing_' + limit] = 'Missing parameter ' + limit
        else:
            limits[limit] = arg
    if len(limits) == 4:
        # bounding box complete. It is possible to query
        resp = es.search_box(limits)
    return json.dumps(resp)


@search.route('/nap/', methods=['GET', 'OPTIONS'])
def search_geo_nap():
    """Performing a geo search for radius around a point using postgres"""
    resp, rd = None, True

    x = request.args.get('x')
    y = request.args.get('y')

    if not x or not y:
        x = request.args.get('lat')
        y = request.args.get('lon')

        if x and y:
            rd = False
        else:
            resp = {'error': 'No coordinates found'}

    # If no error is found, query
    if not resp:
        ds = NapMeetboutenDataSource(dsn=current_app.config['DSN_NAP'])
        resp = ds.query(float(x), float(y), rd=rd, radius=request.args.get('radius'))

    return jsonify(resp)


@search.route('/atlas/', methods=['GET', 'OPTIONS'])
def search_geo_atlas():
    """Performing a geo search for radius around a point using postgres"""
    resp, rd = None, True

    x = request.args.get('x')
    y = request.args.get('y')

    if not x or not y:
        x = request.args.get('lat')
        y = request.args.get('lon')

        if x and y:
            rd = False
        else:
            resp = {'error': 'No coordinates found'}

    # If no error is found, query
    if not resp:
        ds = AtlasDataSource(dsn=current_app.config['DSN_ATLAS'])
        resp = ds.query(float(x), float(y), rd=rd)

    return jsonify(resp)


# Adding cors headers
@search.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response
