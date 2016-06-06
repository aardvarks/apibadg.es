from flask import Flask
from flask import request
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
    defaultOptions = { "labelText": 'value', "labelColour": '555555', "valueColour": '44cc11', "valueText": '\_(ツ)_/¯' }
    options = defaultOptions.copy()
    if request.args.get('api'):
        options.update(get_api_values(request.args.get('api')))
    options.update(request.args.to_dict())

    return generate_badge(options)

def generate_badge(options):
    dwg = svgwrite.Drawing(profile='tiny')

    dwg.add(dwg.rect((0, 0), (87, 20), fill=hex_to_rgb(options['labelColour'])))
    dwg.add(dwg.text(options['labelText'], insert=(6, 14), fill='rgb(255,255,255)', font_family = 'DejaVu Sans,Verdana,Geneva,sans-serif', font_size = '11px'))

    dwg.add(dwg.rect((37, 0), (51, 20), fill=hex_to_rgb(options['valueColour'])))
    dwg.add(dwg.text(options['valueText'], insert=(40.5, 14), fill='rgb(255,255,255)', font_family = 'DejaVu Sans,Verdana,Geneva,sans-serif', font_size = '11px'))

    return dwg.tostring()

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

app.run(debug = True)
