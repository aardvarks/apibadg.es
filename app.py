from flask import Flask
from flask import request
from flask import send_file
from flask import make_response
from io import StringIO
import svgwrite
import requests
import json
import re

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Enter your API URL here: '

@app.route('/badge')
def get_image():
    defaultOptions = { "labelText": 'value', "labelColour": '555555', "valueColour": '44cc11', "valueText": '¯\_(ツ)_/¯' }
    options = defaultOptions.copy()
    if request.args.get('api'):
        options.update(get_api_values(request.args.get('api')))
    options.update(request.args.to_dict())

    return generate_badge(options)

def generate_badge(options):
    dwg = svgwrite.Drawing(profile='tiny')
    font = 'Courier New'
    size = '11px'

    labelWidth = (len(str(options['labelText'])) * 6.6 ) + 15
    dwg.add(dwg.rect((0, 0), (labelWidth, 20), fill=hex_to_rgb(options['labelColour'])))
    dwg.add(dwg.text(options['labelText'], insert=(6, 14), fill='rgb(255,255,255)', font_family = font, font_size = size))

    valueWidth = (len(str(options['valueText'])) * 6.6 ) + 10
    dwg.add(dwg.rect((labelWidth, 0), (valueWidth, 20), fill=hex_to_rgb(options['valueColour'])))
    dwg.add(dwg.text(options['valueText'], insert=(labelWidth + 5, 14), fill='rgb(255,255,255)', font_family = font, font_size = size))

    badge = StringIO()
    dwg.write(badge)
    response=make_response(badge.getvalue())
    response.headers['Content-Type'] = 'image/svg+xml'
    return response

def get_api_values(api):
    r = requests.get(api)
    return json.loads(r.text)

def hex_to_rgb(value):
    if re.match('^(?:[0-9a-fA-F]{3}){1,2}$', value) is not None:
        value = value.lstrip('#')
        def get_int(pos):
            start = pos * 2
            return int(value[start:start+2], 16)
        return 'rgb(' +  str(get_int(0)) + ',' + str(get_int(1)) + ',' + str(get_int(2)) + ')'
    else:
        return('rgb(85,85,85)')

app.run(host='0.0.0.0')
app.run(debug = True)
