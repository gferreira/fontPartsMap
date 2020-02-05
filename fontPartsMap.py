'''
FontParts Object Map
based on the classic [RoboFab Object Map](http://robofab.org/objects/model.html)
'''

import os
import sys
import math
from drawBot import *
from grapefruit import Color
from collections import OrderedDict

FontPartsConnections = [
    ('font',    'info'),
    ('font',    'font lib'),
    ('font',    'groups'),
    ('font',    'kerning'),
    ('font',    'features'),
    ('font',    'layer'),
    ('layer',   'glyph'),
    ('glyph',   'glyph lib'),
    ('glyph',   'anchor'),
    ('glyph',   'component'),
    ('glyph',   'image'),
    ('glyph',   'guideline'),
    ('glyph',   'contour'),
    ('contour', 'point'),
    ('contour', 'bPoint'),
    ('contour', 'segment')
]

class FontPartsColorScheme:

    colorSets = [
        ['font', 'font lib', 'info', 'groups', 'kerning', 'features'],
        ['glyph', 'glyph lib', 'anchor', 'component', 'image', 'guideline', 'contour'],
        ['contour', 'point', 'bPoint', 'segment'],
        ['font', 'layer', 'glyph'],
    ]

    baseColors = {
        # use the original RoboFab colors for Font and Glyph objects
        # calculate colors for all other objects from those two
        'font'  : Color.from_hsl(80, 0.50, 0.49),
        'glyph' : Color.from_hsl(38, 0.91, 0.69),
    }

    def __init__(self):
        self.makeColors()

    def makeColors(self):
        '''
        Calculate colors for all objects.
        Colors are stored in a dict as `grapefruit.Color` objects.

        '''
        colors = self.baseColors.copy()

        # color set 1: Font sub-objects
        for i, obj in enumerate(self.colorSets[0][1:]):
            color = colors['font'].with_hue(colors['font'].hsl[0] + (i+1) * 23)
            colors[obj] = color

        # color set 2: Glyph sub-objects
        for i, obj in enumerate(self.colorSets[1][1:]):
            color = colors['glyph'].with_hue(colors['glyph'].hsl[0] - (i+1) * 15)
            colors[obj] = color

        # color set 3: Contour sub-objects
        for i, obj in enumerate(self.colorSets[2][1:]):
            color = colors['contour'].with_hue(colors['contour'].hsl[0] - (i+1) * 20)
            colors[obj] = color

        # color set 4: Layer
        colors['layer'] = colors['font'].blend(colors['glyph'], percent=0.5)

        self.colors = colors

    @property
    def colorsRGB(self):
        colors = {}
        for obj, color in self.colors.items():
            colors[obj] = color.rgb
        return colors

    @property
    def colorsCMYK(self):
        colors = {}
        for obj, color in self.colors.items():
            colors[obj] = color.cmyk
        return colors

    def drawSwatches(self, pos, cellSize, padding, captions=False):
        x, y = pos
        w, h = cellSize
        save()
        translate(x, y)
        fontSize(w * .12)
        for colorSet in reversed(self.colorSets):
            save()
            for obj in colorSet:
                color = self.colorsRGB[obj]
                fill(*color)
                rect(0, 0, w, h)
                if captions:
                    fill(0)
                    text(obj, (w * .1, h * .2))
                translate(w + padding, 0)
            restore()
            translate(0, (h + padding))
        restore()

class FontPartsMapMaker:

    colors = FontPartsColorScheme()
    colorMode = ['RGB', 'CMYK'][0]

    connections = FontPartsConnections

    # radius for sub-objects
    radius1 = 50

    # radius for main objects: Font & Glyph
    radius2 = 70

    # distance between Font/Glyph and its sub-objects
    length1 = 160

    # distance between Font/Glyph and Layer
    length2 = 200

    # no longer used?
    length3 = 170 

    # angle between Font sub-objects
    angle1  = 180 / 3
    angleStart1 = 0

    # angle between Glyph sub-objects
    angle2  = 180 / 4
    angleStart2 = 0

    # angle between Contour sub-objects
    angle3  = 180 / 3.5
    angleStart3 = 0

    # font settings
    font = 'RoboType-Bold'
    fontSize1 = 18 # sub-objects
    fontSize2 = 32 # main objects: Font/Glyph

    # toggle object names
    textDraw  = True
    textColor = 1,

    # connection lines
    linesStrokeColor = 0.6,
    linesStrokeWidth = 4
    linesDash = 3, 7

    # deprecated
    # circlesStrokeColor = 0,
    # circlesStrokeWidth = 3

    # shadow settings
    circlesShadowDraw     = True
    circlesShadowDistance = 10, 0
    circlesShadowBlur     = 15
    circlesShadowColor    = 0, 0.25

    # settings for dimmed objects
    dimColor = 0.5,
    dimObjects = []

    # randomize positions
    randomness = 0

    tree = {
        'font'    : ['font lib', 'info', 'groups', 'kerning', 'features'],
        'glyph'   : ['glyph lib', 'anchor', 'component', 'image', 'guideline', 'contour'],
        'contour' : ['point', 'bPoint', 'segment'],
    }

    positions = {}

    def setAttributes(self, attrsDict):
        '''
        Set map attributes from a given dictionary.

        '''
        for key, value in attrsDict.items():
            setattr(self, key, value)

    def makePositions(self, pos):
        '''
        Calculate object positions and store them in a dict.

        '''
        x, y = pos

        # font etc.
        xFont, yFont = x, y
        self.positions['font'] = xFont, yFont
        for i, obj in enumerate(self.tree['font']):
            x_ = xFont + cos(radians(self.angleStart1 + self.angle1 * i)) * self.length1
            y_ = yFont + sin(radians(self.angleStart1 + self.angle1 * i)) * self.length1
            self.positions[obj] = x_, y_

        # layer
        xLayer = xFont + cos(radians(self.angleStart0)) * self.length2
        yLayer = yFont + sin(radians(self.angleStart0)) * self.length2

        self.positions['layer'] = xLayer, yLayer

        # glyph etc.
        xGlyph = xLayer + cos(radians(self.angleStart4)) * self.length2
        yGlyph = yLayer + sin(radians(self.angleStart4)) * self.length2

        self.positions['glyph'] = xGlyph, yGlyph
        for i, obj in enumerate(self.tree['glyph']):
            x_ = xGlyph + cos(radians(self.angleStart2 - self.angle2 * i)) * self.length1
            y_ = yGlyph + sin(radians(self.angleStart2 - self.angle2 * i)) * self.length1
            self.positions[obj] = x_, y_

        # point etc.
        xContour, yContour = self.positions['contour']
        length = self.length1 - (self.radius2 - self.radius1)
        for i, obj in enumerate(self.tree['contour']):
            x_ = xContour + cos(radians(self.angleStart3 + self.angle3 * i)) * length
            y_ = yContour + sin(radians(self.angleStart3 + self.angle3 * i)) * length
            self.positions[obj] = x_, y_

        # randomize
        if self.randomness != 0:
            for obj, (x, y) in self.positions.items():
                x += randint(-self.randomness, self.randomness)
                y += randint(-self.randomness, self.randomness)
                self.positions[obj] = x, y

    def drawLines(self):
        '''
        Draw lines connecting objects to sub-objects.

        '''
        if not self.linesDraw:
            return

        save()

        for obj1, obj2 in self.connections:

            if self.linesGradient:

                B = BezierPath()
                B.moveTo(self.positions[obj1])
                B.lineTo(self.positions[obj2])
                B2 = B.expandStroke(self.linesStrokeWidth)

                r1 = self.radius1 if obj1 not in ['font', 'glyph'] else self.radius2
                r2 = self.radius1 if obj2 not in ['font', 'glyph'] else self.radius2

                dx = self.positions[obj2][0] - self.positions[obj1][0]
                dy = self.positions[obj2][1] - self.positions[obj1][1]

                aRadians = math.atan2(dy, dx)

                x1 = self.positions[obj1][0] + r1 * cos(aRadians)
                y1 = self.positions[obj1][1] + r1 * sin(aRadians)

                x2 = self.positions[obj2][0] - r2 * cos(aRadians)
                y2 = self.positions[obj2][1] - r2 * sin(aRadians)

                if self.colorMode == 'CMYK':
                    c1 = self.colors.colorsCMYK[obj1] if not obj1 in self.dimObjects else self.dimColor
                    c2 = self.colors.colorsCMYK[obj2] if not obj2 in self.dimObjects else self.dimColor
                else:
                    c1 = self.colors.colorsRGB[obj1] if not obj1 in self.dimObjects else self.dimColor
                    c2 = self.colors.colorsRGB[obj2] if not obj2 in self.dimObjects else self.dimColor

                linearGradient(
                    (x1, y1), (x2, y2),
                    [c1, c2],
                    [0, 1])

                drawPath(B2)

            else:
                lineDash(*self.linesDash)
                stroke(*self.linesStrokeColor)
                strokeWidth(self.linesStrokeWidth)
                lineCap('round')
                line(self.positions[obj1], self.positions[obj2])

        restore()

    def drawCircles(self):
        '''
        Draw a circle representing each object.

        '''
        save()
        stroke(None)

        if self.circlesShadowDraw:
            shadow(self.circlesShadowDistance, blur=self.circlesShadowBlur, color=self.circlesShadowColor)

        for obj, pos in self.positions.items():
            x, y = pos
            r = self.radius1 if obj not in ['font', 'glyph'] else self.radius2

            if self.colorMode == 'CMYK':
                c = self.colors.colorsCMYK[obj] if obj not in self.dimObjects else self.dimColor
            else:
                c = self.colors.colorsRGB[obj] if obj not in self.dimObjects else self.dimColor

            fill(*c)
            oval(x - r, y - r, r*2, r*2)

        restore()

    def drawCaptions(self):
        '''
        Draw the name of each object.
        
        '''
        if not self.textDraw:
            return

        save()
        fill(*self.textColor)
        font(self.font)

        for obj in self.positions.keys():
            x, y = self.positions[obj]
            c = self.colors.colors[obj].darker(0.4)
            c = c.cmyk if self.colorMode == 'CMYK' else c.rgb
            c += (0.7,)
            shadow((2, -2), blur=5, color=c)

            if obj not in ['font', 'glyph']:
                r = self.radius1
                fontSize(self.fontSize1)
                h = r - self.fontSize1 * -0.6

            else:
                r = self.radius2
                fontSize(self.fontSize2)
                h = r - self.fontSize2 * -0.65

            if len(obj.split('_')) > 1:
                obj = obj.split('_')[-1]

            textBox(obj, (x - r, y - r, r * 2, h), align='center')

        restore()

    def draw(self, pos=(0, 0)):
        '''
        Draw the FontParts object map at a given position.

        The origin point is the center of the Font circle.

        '''
        self.makePositions(pos)
        self.drawLines()
        self.drawCircles()
        self.drawCaptions()

class FontPartsMapUI:

    def __init__(self):

        M = FontPartsMap()

        Variable([
            dict(name="x",           ui="Slider", args=dict(value=300, minValue=0,  maxValue=1000)),
            dict(name="y",           ui="Slider", args=dict(value=400, minValue=0,  maxValue=1000)),
            dict(name="radius1",     ui="Slider", args=dict(value=M.radius1,     minValue=M.radius1*0.5,     maxValue=M.radius1*1.5)),
            dict(name="radius2",     ui="Slider", args=dict(value=M.radius2,     minValue=M.radius2*0.5,     maxValue=M.radius2*1.5)),
            dict(name="length1",     ui="Slider", args=dict(value=M.length1,     minValue=M.length1*0.5,     maxValue=M.length1*1.5)),
            dict(name="length2",     ui="Slider", args=dict(value=M.length2,     minValue=M.length2*0.5,     maxValue=M.length2*1.5)),
            dict(name="angle1",      ui="Slider", args=dict(value=M.angle1,      minValue=M.angle1*0.5,      maxValue=M.angle1*1.5)),
            dict(name="angleStart1", ui="Slider", args=dict(value=M.angleStart1, minValue=M.angleStart1*0.5, maxValue=M.angleStart1*1.5)),
            dict(name="angle2",      ui="Slider", args=dict(value=M.angle2,      minValue=M.angle2*0.5,      maxValue=M.angle2*1.5)),
            dict(name="angleStart2", ui="Slider", args=dict(value=M.angleStart2, minValue=M.angleStart2*0.5, maxValue=M.angleStart2*1.5)),
            dict(name="angle3",      ui="Slider", args=dict(value=M.angle3,      minValue=M.angle3*0.5,      maxValue=M.angle3*1.5)),
            dict(name="angleStart3", ui="Slider", args=dict(value=M.angleStart3, minValue=M.angleStart3*0.5, maxValue=M.angleStart3*1.5)),
            dict(name="randomness",  ui="Slider", args=dict(value=M.randomness,  minValue=0, maxValue=10)),
        ], globals())

        M.radius1 = radius1
        M.radius2 = radius2
        M.length1 = length1
        M.length2 = length2
        M.length3 = length3

        M.angle1 = angle1
        M.angle2 = angle2
        M.angle3 = angle3

        M.angleStart1 = angleStart1
        M.angleStart2 = angleStart2
        M.angleStart3 = angleStart3

        M.randomness = int(randomness)

        M.draw((x, y))

class FontPartsMap(FontPartsMapMaker):
    
    def __init__(self):
        length = 180
        angle  = 50
        mapAttrs = {
            'radius1'           : 60,
            'radius2'           : 85,
            'length1'           : length,
            'length2'           : length,
            'angle1'            : angle,
            'angle2'            : angle,
            'angle3'            : angle * 1.13,
            'angleStart0'       : 0,
            'angleStart1'       : 54,
            'angleStart2'       : 125,
            'angleStart3'       : 180,
            'angleStart4'       : 0,
            'randomness'        : 0,
            'linesDraw'         : True,
            'linesGradient'     : True,
            'linesStrokeWidth'  : 10,
            'linesStrokeColor'  : (0.8,),
            'linesDash'         : (1, 5),
            'circlesShadowDraw' : False,
            'textDraw'          : True,
        }
        # self.map = FontPartsMapMaker()
        self.setAttributes(mapAttrs)

if __name__ == '__main__':

    size(1000, 700)
    translate(300, 410)
    M = FontPartsMap()
    M.draw()

