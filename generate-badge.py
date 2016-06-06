import svgwrite
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Enter your API URL here: '

@app.route('/badge')
def get_image():
    return generateBadge(False, 'build', '555555', 'passing', '44cc11')

def generateBadge(apiURL, labelText, labelColour, valueText, valueColour):
    dwg = svgwrite.Drawing(profile='tiny')

    dwg.add(dwg.rect((0, 0), (87, 20), fill=hex_to_rgb(labelColour)))
    dwg.add(dwg.text(labelText, insert=(6, 14), fill='rgb(255,255,255)', font_family = 'DejaVu Sans,Verdana,Geneva,sans-serif', font_size = '11px'))

    dwg.add(dwg.rect((37, 0), (51, 20), fill=hex_to_rgb(valueColour)))
    dwg.add(dwg.text(valueText, insert=(40.5, 14), fill='rgb(255,255,255)', font_family = 'DejaVu Sans,Verdana,Geneva,sans-serif', font_size = '11px'))

    return dwg.tostring()

def hex_to_rgb(value):
    value = value.lstrip('#')
    def get_int(pos):
        start = pos * 2
        return int(value[start:start+2], 16)
    return 'rgb(' +  str(get_int(0)) + ',' + str(get_int(1)) + ',' + str(get_int(2)) + ')'

app.run(debug = True)
