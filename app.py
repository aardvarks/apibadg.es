from flask import Flask
from flask import request
from flask import send_file
from flask import make_response
from io import StringIO
import svgwrite
import requests
import hashlib
import urllib
import json
import re

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '''
    <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
    </head>
    <pre>
        <form method=get action=/badge><br/>
            Create an API using this spec to get dynamic badges:

              {
                'labelText': 'users active',
                'labelColour': '555555',
                'valueText': userCount,
                'valueColour': '44cc11',
              }

            Api URL: <input name=api type=text /><br/>

            And/or override with these fields:

            Label Colour: <input name=labelColour type=text /><br/>
            Label Text: <input name=labelText type=text /><br/>
            Value Colour: <input name=valueColour type=text /><br/>
            Value Text: <input name=valueText type=text /><br/>
            <input type=submit onsumbit=removeEmpty() /><br/>
        </form>
    </pre>
    <script>
        $('form').submit(function() {
            $(':input', this).each(function() {
                this.disabled = !($(this).val())
            })
        })
    </script>
    '''

@app.route('/badge')
def get_image():
    defaultOptions = { "labelText": 'value', "labelColour": '555555', "valueColour": '44cc11', "valueText": '¯\_(ツ)_/¯' }
    options = defaultOptions.copy()
    if request.args.get('api'):
        url=urllib.parse.unquote(request.args.get('api'))
        if not url.startswith('http'):
            url = 'http://' + url
        options.update(get_api_values(url))
    options.update(request.args.to_dict())

    return generate_badge(options)

def generate_badge(options):
    labelWidth = (len(str(options['labelText'])) * 6.6 ) + 10
    valueWidth = (len(str(options['valueText'])) * 6.6 ) + 10

    dwg = svgwrite.Drawing(profile='tiny', size=(labelWidth + valueWidth, 20))
    font = 'Courier New'
    size = '11px'

    dwg.add(dwg.rect((0, 0), (labelWidth, 20), fill=hex_to_rgb(options['labelColour'])))
    dwg.add(dwg.text(options['labelText'], insert=(6, 14), fill='rgb(255,255,255)', font_family = font, font_size = size))

    dwg.add(dwg.rect((labelWidth, 0), (valueWidth, 20), fill=hex_to_rgb(options['valueColour'])))
    dwg.add(dwg.text(options['valueText'], insert=(labelWidth + 5, 14), fill='rgb(255,255,255)', font_family = font, font_size = size))

    badge = StringIO()
    dwg.write(badge)
    response=make_response(badge.getvalue())
    response.headers['Content-Type'] = 'image/svg+xml'
    response.headers['Cache-Control'] = 'no-cache'
    etag = hashlib.sha1(dwg.tostring().encode('utf-8')).hexdigest()
    response.set_etag(etag)
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
