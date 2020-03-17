import wand.image
import wand.color


base_code = """
<svg xmlns="http://www.w3.org/2000/svg" height="400px" width="200px" >
    ###PATTERN###
    
    ###SHAPE###

    
</svg>
"""

pattern = """
<defs>
    <pattern id="shade" x="0" y="0" width=".25" height=".03">
        <rect x="0" y="1" width="50" height="3" fill="black"/>
    </pattern>
</defs>
    """

oval = base_code.replace("###SHAPE###", """
<path d="
    M 10 110
    c0,-125 175,-125 175,0
    v180
    c0, 125 -175, 125 -175,0
    z" 
    stroke="black" stroke-width="8" fill="none"/>
""")
diamond = base_code.replace("###SHAPE###", """
<polygon points="100,15 195,200 100,385 5,200" 
    stroke="black" stroke-width="8" fill="none"/>
""")

# Requires a different viewbox
squiggle = """
<svg xmlns="http://www.w3.org/2000/svg" height="400px" width="200px" viewBox="0 0 100 250">
    ###PATTERN###
    
<path d="
    M10,115
    c-19,-40,-7,-75,39,-97.5
    s57,13,42.5,31.5
    s-24,41,-4,83.5
    s10.5,80,-40,101.5
    s-55,-19,-36,-37.5
    s9,-66,-0.75,-79.5
    Z "
    stroke="black" stroke-width="4" fill="none"/>
    
    </svg>
"""


def writeSVG(color="indigo", fill="solid", shape="diamond", outFile="shape.svg"):
    if shape == "squiggle":
        code = squiggle
    elif shape == "oval":
        code = oval
    else:
        code = diamond

    code = code.replace('stroke="black"', 'stroke="{}"'.format(color))

    if fill == "shade":
        p = pattern.replace('fill="black"', 'fill="{}"'.format(color))
        code = code.replace("###PATTERN###", p)
        code = code.replace('fill="none"', 'fill="url(#shade)"')
    elif fill == "solid":
        code = code.replace('fill="none"', 'fill="{}"'.format(color))

    text_file = open(outFile, "w")
    text_file.write(code)
    text_file.close()

    return outFile


def buildCard(number=1, color="indigo", fill="solid", shape="diamond"):
    """

    :param number:
    :param color:
    :param fill:
    :param shape:
    :return: the filename of the output file
    """
    svg = writeSVG(color, fill, shape)
    with wand.image.Image(filename=svg) as img:
        with wand.image.Image(width=800, height=500, background=wand.color.Color("WHITE")) as output:
            if number == 1:
                output.composite(image=img, left=300, top=50)
            if number == 2:
                output.composite(image=img, left=175, top=50)
                output.composite(image=img, left=425, top=50)
            if number == 3:
                output.composite(image=img, left=50, top=50)
                output.composite(image=img, left=300, top=50)
                output.composite(image=img, left=550, top=50)
            filename = color[0]+shape[0]+fill[4]+str(number)+".png"
            output.save(filename="photos/"+filename)
    return filename

def createSetCards():
    colors = ["indigo","green","crimson"]
    shapes = ["diamond","squiggle", "oval"]
    fills = ["solid", "shade", "empty"]
    for i in range(3):
        i +=1;
        for color in colors:
            for shape in shapes:
                for fill in fills:
                    buildCard(i, color, fill, shape)


if __name__ == "__main__":
    createSetCards()



