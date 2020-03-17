
base_code = """
<svg xmlns="http://www.w3.org/2000/svg" height="400px" width="200px" viewBox="0 0 100 250">
    <defs>
        <pattern id="shade" x="0" y="0" width=".25" height=".03">
            <rect x="0" y="1" width="50" height="3" fill="indigo"/>
        </pattern>
    </defs>
    
    ###SHAPE###

    
</svg>
"""
squiggle = """
<path d="
    M10,115
    c-19,-40,-7,-75,39,-97.5
    s57,13,42.5,31.5
    s-24,41,-4,83.5
    s10.5,80,-40,101.5
    s-55,-19,-36,-37.5
    s9,-66,-0.75,-79.5
    Z "
    stroke="black" stroke-width="2" fill="url(#shade)"/>
"""
oval = """
<path d="
    M 10 110
    c0,-125 175,-125 175,0
    v180
    c0, 125 -175, 125 -175,0
    z" 
    stroke="black" stroke-width="3" fill="none"/>
"""
diamond = """
<polygon points="105,15 200,200 105,385 10,200" 
    stroke="black" stroke-width="3" fill="indigo"/>
"""

text_file = open("sample.svg", "w")
n = text_file.write(base_code.replace("###SHAPE###", squiggle))
text_file.close()

svg_code = base_code.replace("###SHAPE###", squiggle)
"""
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

drawing = svg2rlg("sample.svg")
renderPM.drawToFile(drawing, "file.png", fmt="PNG")
"""


import cairo
from rsvg import *

def convert(data, ofile, maxwidth=0, maxheight=0):

    svg = rsvgHandle(data)

    x = width = svg.props.width
    y = height = svg.props.height
    print("actual dims are " + str((width, height)))
    print("converting to " + str((maxwidth, maxheight)))

    yscale = xscale = 1

    if (maxheight != 0 and width > maxwidth) or (maxheight != 0 and height > maxheight):
        x = maxwidth
        y = float(maxwidth)/float(width) * height
        print ("first resize: " + str((x, y)))
        if y > maxheight:
            y = maxheight
            x = float(maxheight)/float(height) * width
            print("second resize: " + str((x, y)))
        xscale = float(x)/svg.props.width
        yscale = float(y)/svg.props.height

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, x, y)
    context = cairo.Context(surface)
    context.scale(xscale, yscale)
    svg.render_cairo(context)
    surface.write_to_png(ofile)

#convert("sample.svg", 200,400)
